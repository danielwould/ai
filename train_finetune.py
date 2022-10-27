import pandas as pd
import torch
from torch.utils.data import Dataset, random_split
from transformers import GPT2Tokenizer, TrainingArguments, Trainer, GPTNeoForCausalLM

torch.manual_seed(42)
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-350M", bos_token='<|start|>',
                                          eos_token='<|end|>', pad_token='<|pad|>')
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-350M").cuda()
model.resize_token_embeddings(len(tokenizer))
scenes = pd.read_csv('./scripts/scenes.csv')
max_length=0

for scene in scenes['SceneText']:
    try:
        length = len(tokenizer.encode(scene[:512]))
        if length > max_length:
            max_length=length
    except:
        print("Exception calculating max_length")


class ScenesDataset(Dataset):
    def __init__(self, scenes, tokenizer, max_length):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for scene in scenes:
            try:
                encodings_dict = tokenizer('<|start|>' + scene['SceneText'] + '<|end|>', truncation=True,
                                        max_length=max_length, padding="max_length")
                self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
                self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
                self.labels.append(torch.tensor(scene['Labels']))
            except:
                print ("ignore nan errors")

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx], self.labels[idx]


dataset = ScenesDataset(scenes, tokenizer, max_length=max_length)
train_size = int(0.9 * len(dataset))
train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])
training_args = TrainingArguments(output_dir='./results', num_train_epochs=5, logging_steps=5000, save_steps=5000,
                                  per_device_train_batch_size=2, per_device_eval_batch_size=2,
                                  warmup_steps=100, weight_decay=0.01, logging_dir='./logs')
Trainer(model=model, args=training_args, train_dataset=train_dataset,
        eval_dataset=val_dataset, data_collator=lambda data: {'input_ids': torch.stack([f[0] for f in data]),
                                                              'attention_mask': torch.stack([f[1] for f in data]),
                                                              'labels': torch.stack([f[0] for f in data])}).train()
generated = tokenizer("<|startoftext|> ", return_tensors="pt").input_ids.cuda()
model.save_pretrained("./police_ai/")
sample_outputs = model.generate(generated, do_sample=True, top_k=50, 
                                max_length=300, top_p=0.95, temperature=1.9, num_return_sequences=20)
for i, sample_output in enumerate(sample_outputs):
    print("{}: {}".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))