from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
#from . import db
#import pandas as pd
import torch
from torch.utils.data import Dataset, random_split
from transformers import GPT2Tokenizer, GPTNeoForCausalLM
import logging
import json
#import time
main = Blueprint('main', __name__)

torch.manual_seed(23)
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125M", bos_token='<|startoftext|>',
                                          eos_token='<|endoftext|>', pad_token='<|pad|>')
model = GPTNeoForCausalLM.from_pretrained("./police_ai").cuda()

logger = logging.getLogger("ui-log")
hdlr = logging.FileHandler('./{}.log'.format("ui-log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/.well-known/<path:path>')
def send_report(path):
    logger.info("request for {}".format(path))
    file = "/static/certs/"+path
    logger.info(file)
    f = open("/home/wouldd/code/web_ui/"+file,"r")
    logger.info(f.read())
    return send_file("/home/wouldd/code/web_ui/"+file)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/generate')
@login_required
def generate():
    return render_template('ai-generate.html', name=current_user.name)

@main.route('/generate', methods=['POST'])
@login_required
def generate_post():
    data = request.get_json()
    
    logger.info("generate {}".format(data))
    temp = data['weirdness']
    temp = round(temp/10,1)
    random_seed = data['random_seed']
    scene_count = data['scene_count']
    torch.manual_seed(random_seed)

    generated = tokenizer("<|startoftext|> "+data['prompt'], return_tensors="pt").input_ids.cuda()
    sample_outputs = model.generate(generated, do_sample=True, top_k=50, 
                                max_length=300, top_p=0.95, temperature=temp, num_return_sequences=scene_count)
    response="{\"generated_text\":{"                    
    for i, sample_output in enumerate(sample_outputs):
        logger.info("{}:\"".format(i)+json.dumps(tokenizer.decode(sample_output, skip_special_tokens=True))+"\"")
        response=response+"\"{}\":".format(i)+json.dumps(tokenizer.decode(sample_output, skip_special_tokens=True))
        if i<scene_count-1:
            response=response+","
    response=response+"}}"
    logger.info(response)
    return response