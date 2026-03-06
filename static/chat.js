let emotionChart = null
let timelineChart = null

let timelineLabels = []
let timelineValues = []


/* MESSAGE RENDER FUNCTIONS */

function addUserMessage(text){

const chatbox = document.getElementById("chatbox")

chatbox.innerHTML += `
<div class="message-row user-row">
<div class="message user">${text}</div>
<div class="avatar">
<img src="/static/images/user-avatar.svg" class="user-avatar">
</div>
</div>
`

scrollChat()

}

function addBotMessage(text, emotion, confidence){

const chatbox = document.getElementById("chatbox")

const emoji = getEmoji(emotion)

chatbox.innerHTML += `
<div class="message-row bot-row">

<div class="avatar">
<i data-lucide="cpu"></i>
</div>

<div>

<div class="message bot">${text}</div>

<div class="emotion-badge">
${emoji} ${emotion} • ${Math.round(confidence*100)}%
</div>

</div>

</div>
`

lucide.createIcons()
scrollChat()

}


/* TYPING INDICATOR */

function showTyping(){

const chatbox = document.getElementById("chatbox")

chatbox.innerHTML += `
<div class="message-row bot-row" id="typing">

<div class="avatar">
<img src="/static/images/emora-avatar.png" class="bot-avatar">
</div>

<div class="message bot">

<div class="typing">
<span></span>
<span></span>
<span></span>
</div>

</div>

</div>
`

lucide.createIcons()
scrollChat()

}

function removeTyping(){

const typing = document.getElementById("typing")
if(typing) typing.remove()

}


/* SEND MESSAGE */

async function sendMessage(){

const input = document.getElementById("message")
const message = input.value.trim()

if(message === "") return

addUserMessage(message)

input.value = ""

showTyping()

try{

const response = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:message})
})

const data = await response.json()

removeTyping()

addBotMessage(data.response, data.emotion, data.confidence)

speakResponse(data.response)

timelineLabels.push("Msg " + (timelineLabels.length + 1))
timelineValues.push(data.confidence)

updateTimeline()

loadHistory()
refreshAnalytics()

}catch(error){

removeTyping()

addBotMessage("Server error. Please try again.","neutral",0)

}

}


/* ENTER KEY */

function handleKey(e){

if(e.key === "Enter"){
e.preventDefault()
sendMessage()
}

}


/* SCROLL CHAT */

function scrollChat(){

const chatbox = document.getElementById("chatbox")

setTimeout(()=>{
chatbox.scrollTop = chatbox.scrollHeight
},50)

}


/* EMOJI MAP */

function getEmoji(emotion){

const emojis = {
joy:"😊",
sadness:"😢",
anger:"😡",
fear:"😨",
love:"❤️",
surprise:"😲",
neutral:"🙂"
}

return emojis[emotion] || "🙂"

}


/* NEW CHAT */

async function newChat(){

await fetch("/new_chat")

document.getElementById("chatbox").innerHTML = ""

timelineLabels=[]
timelineValues=[]

if(timelineChart){
timelineChart.destroy()
timelineChart=null
}

}


/* LOAD HISTORY */

async function loadHistory(){

const response = await fetch("/history")
const chats = await response.json()

const historyDiv = document.querySelector(".history")

if(!historyDiv) return

historyDiv.innerHTML=""

chats.forEach(chat=>{

const item=document.createElement("div")

item.innerText=chat.title

item.onclick=()=>loadChat(chat.session)

historyDiv.appendChild(item)

})

}


/* CLEAR HISTORY */

async function clearHistory(){

await fetch("/clear_history")

const historyDiv=document.querySelector(".history")

if(historyDiv) historyDiv.innerHTML=""

}


/* ANALYTICS */

async function refreshAnalytics(){

const response=await fetch("/analytics")
const data=await response.json()

drawEmotionChart(data)

const total = Object.values(data).reduce((a,b)=>a+b,0)

const totalElement=document.getElementById("totalMessages")

if(totalElement) totalElement.innerText = total

}


/* EMOTION BAR CHART */

function drawEmotionChart(data){

if(!data || Object.keys(data).length === 0){
return
}

const canvas = document.getElementById("emotionChart")
if(!canvas) return

const ctx = canvas.getContext("2d")

if(emotionChart){
emotionChart.destroy()
}

emotionChart = new Chart(ctx,{
type:"bar",
data:{
labels:Object.keys(data),
datasets:[{
data:Object.values(data),
backgroundColor:"#6366f1"
}]
},
options:{
responsive:true,
maintainAspectRatio:false,
plugins:{legend:{display:false}},
scales:{y:{beginAtZero:true}}
}
})

}

/* EMOTION TIMELINE */

function updateTimeline(){

const canvas=document.getElementById("emotionTimeline")

if(!canvas) return

const ctx=canvas.getContext("2d")

if(timelineChart){
timelineChart.destroy()
}

timelineChart=new Chart(ctx,{
type:"line",
data:{
labels:timelineLabels,
datasets:[{
data:timelineValues,
borderColor:"#6366f1",
backgroundColor:"rgba(99,102,241,0.2)",
tension:0.4
}]
},
options:{
responsive:true,
maintainAspectRatio:false,
plugins:{legend:{display:false}},
scales:{y:{min:0,max:1}}
}
})

}


/* LOAD CHAT SESSION */

async function loadChat(session){

const response = await fetch("/load_chat/"+session)

const chats = await response.json()

const chatbox = document.getElementById("chatbox")

chatbox.innerHTML=""

chats.forEach(c=>{

addUserMessage(c.user)

addBotMessage(c.bot,c.emotion,c.confidence)

})

scrollChat()

}


/* VOICE INPUT */

function startListening(){

const micButton = document.getElementById("micButton")

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)()

recognition.lang = "en-US"

micButton.classList.add("mic-listening")

recognition.start()

recognition.onresult = function(event){

const transcript = event.results[0][0].transcript

document.getElementById("message").value = transcript

micButton.classList.remove("mic-listening")

sendMessage()

}

recognition.onend = function(){
micButton.classList.remove("mic-listening")
}

}


/* TEXT TO SPEECH */

function speakResponse(text){

const speech = new SpeechSynthesisUtterance()

speech.text = text
speech.lang = "en-US"

window.speechSynthesis.speak(speech)

}


/* AUDIO FILE */

async function uploadAudio(){

const fileInput=document.getElementById("audioFile")

if(fileInput.files.length===0){
alert("Select audio file")
return
}

const formData=new FormData()

formData.append("audio", fileInput.files[0])

const response = await fetch("/audio",{
method:"POST",
body:formData
})

const data = await response.json()

addUserMessage(data.transcript)

addBotMessage(data.response,data.emotion,data.confidence)

timelineLabels.push("Msg " + (timelineLabels.length + 1))
timelineValues.push(data.confidence)

updateTimeline()

loadHistory()
refreshAnalytics()

scrollChat()
}


/* PAGE LOAD */

window.onload=function(){

loadHistory()

document.getElementById("message").value=""

setTimeout(()=>{
updateTimeline()
},300)

lucide.createIcons()

}