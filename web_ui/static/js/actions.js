async function update_generated_text(text){
    var textbox = document.getElementById('ai-output');
    console.log(text);
    
    let generated_results="";
    
    Object.keys(text['generated_text']).forEach(function(key) {
        console.log(text['generated_text'][key]);
        generated_results=generated_results+text['generated_text'][key]+"<br/>==========<br/>"
      });
    textbox.innerHTML =generated_results.replace(/\n/g, "<br />");;
    document.getElementById("loader").style.display = "none";
}

async function generate_text(elem_id){
    document.getElementById("loader").style.display = "";
    var prompt = document.getElementById("prompt").value;
    
    var scene_count = document.getElementById("generate-count");
    var weirdness = document.getElementById("weirdness");
    var random_seed = document.getElementById("random-seed");
    
    payload = '{"prompt":'+JSON.stringify(prompt)+',"scene_count":'+scene_count.value+',"weirdness":'+weirdness.value+',"random_seed":'+random_seed.value+'}'
    console.log(payload);
    response = post_command('/generate', payload);
    response.then(data =>{
        console.log(data); // JSON data parsed by `data.json()` call
        update_generated_text(data);
    });
    
    
}
async function post_command(url,payload){
    const response = await fetch(url, {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: payload
    });
    return response.json()
}