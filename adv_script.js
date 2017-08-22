var MAIN_CONTENT;
var SAVE_CONTENT;
var CONTENT_PARSED = [];
var CURRENT_LOC;
var SAVE_HEADER = "NA";

function changeBackground() {
    document.getElementsByTagName("body")[0].style.background = "url(Images/ruslan-kim-4.jpg) no-repeat center center fixed";
    document.getElementsByTagName("body")[0].style.backgroundSize = "cover";
}

function option(elem,id) {
    var node = document.createElement("div");
    node.className = "ChoiceDisplay";
    node.innerHTML = "<img src='Icons/key.svg' style='display: inline; padding-right: 10px; height: 20px; float: left;'/>";
    node.innerHTML += elem.innerHTML;
    document.getElementById("MainContainer").appendChild(node);
    
    addContent(id);
    
}

function addContent(id) {
    var choiceHolder;
    var node = document.createElement("div");
    node.className = "TextDisplay";
    node.innerHTML = "<img src='Icons/gem.svg' style='display: inline; padding-right: 10px; height: 20px; float: left;'/>";
    //node.innerHTML += "Du hast Option " + id.toString().substring(4,id.toString().length) + " gewählt!";
    var choiceIdx = parseInt(id)-1;
    var newHeader = CURRENT_LOC.choices[choiceIdx].substring(0,CURRENT_LOC.choices[choiceIdx].indexOf(">"));

    for (var i = 0; i < CONTENT_PARSED.length; i++) {
        if(CONTENT_PARSED[i].header === newHeader) {
            CURRENT_LOC = CONTENT_PARSED[i];
            for(var j = 0; j < CONTENT_PARSED[i].content.length; j++) {
                node.innerHTML += CONTENT_PARSED[i].content[j];
                if(j+1 < CONTENT_PARSED[i].content.length) {
                    node.innerHTML += "<br/>";
                }
            }
        }
    }
    
    
    document.getElementById("MainContainer").appendChild(node);
    window.scrollTo(0,document.body.scrollHeight);
    
    document.getElementById("ChoiceContainer").innerHTML = "";
    for (var j = 0; j < CURRENT_LOC.choices.length; j++) {
        var node = document.createElement("p");
        node.className = "TextBlock";
        choiceHolder = CURRENT_LOC.choices[j];
        node.innerHTML = (j+1).toString() + ". ";
        node.innerHTML += choiceHolder.substring(choiceHolder.indexOf(">")+1,choiceHolder.length);
        node.id = (j+1).toString();
        node.onclick = function() {
            option(this,this.id);
        }
        
        document.getElementById("ChoiceContainer").appendChild(node);
    }
    window.scrollTo(0,document.body.scrollHeight);
    
}

function getSave() {
    var choiceHolder;
    myFileList = document.getElementById("SaveLoader");
    
    for (var i = 0; i < myFileList.files.length; i++) {
        
        var file = myFileList.files[0],read = new FileReader();

        read.readAsBinaryString(file);

        read.onloadend = function(){
            SAVE_CONTENT = read.result;
            restoreSave(SAVE_CONTENT);
        }
                
    }
}

function showCredits() {
    document.getElementById("CreditContent").style.display = "inline";
    document.getElementById("StartIcons").style.display = "none";
}

function creditReturn() {
    document.getElementById("StartIcons").style.display = "inline";
    document.getElementById("CreditContent").style.display = "none";
}

function getFiles() {
    var choiceHolder;
    myFileList = document.getElementById("FileLoader");
    
    for (var i = 0; i < myFileList.files.length; i++) {
        
        var file = myFileList.files[0],read = new FileReader();

        read.readAsBinaryString(file);

        read.onloadend = function(){
            MAIN_CONTENT = read.result;
            parseContent(MAIN_CONTENT);
            
            if(SAVE_HEADER === "NA") {
                CURRENT_LOC = CONTENT_PARSED[0];
            } else {
                for(var j = 0; j < CONTENT_PARSED.length; j++) {
                    if(SAVE_HEADER === CONTENT_PARSED[j].header) {
                        CURRENT_LOC = CONTENT_PARSED[j];
                        break;
                    }
                }
                if(CURRENT_LOC.length == 0) {
                    CURRENT_LOC = CONTENT_PARSED[0];
                }
            }
            
            
            var final_content = "";
            for (var j = 0; j < CURRENT_LOC.content.length; j++) {
                final_content += CURRENT_LOC.content[j] + "<br/>";
            }
            
            for (var j = 0; j < CURRENT_LOC.choices.length; j++) {
                var node = document.createElement("p");
                node.className = "TextBlock";
                choiceHolder = CURRENT_LOC.choices[j];
                node.innerHTML = (j+1).toString() + ". ";
                node.innerHTML += choiceHolder.substring(choiceHolder.indexOf(">")+1,choiceHolder.length);
                node.id = (j+1).toString();
                node.onclick = function() {
                    option(this,this.id);
                }
                
                document.getElementById("ChoiceContainer").appendChild(node);
            }
            
            document.getElementById("MainText").innerHTML = "<img src='Icons/gem.svg' style='display: inline; padding-right: 10px; height: 20px; float: left;'/>";
            document.getElementById("MainText").innerHTML += final_content;
            
            
            document.getElementById("MainContainer").style.display = "inline";
            document.getElementById("ChoiceContainer").style.display = "block";
            document.getElementById("FileLoader").style.display = "none";
            document.getElementById("Navbar").style.display = "inline";
            document.getElementById("StartIcons").style.display = "none";
            
            
            // document.getElementById("MainText").innerHTML = "<img src='Icons/gem.svg' style='display: inline; height: 20px; float: left;'/>"
            // document.getElementById("MainText").innerHTML += MAIN_CONTENT.replace(/(?:\r\n|\r|\n)/g, '<br />');
        }
                
    }
}

function parseContent(content) {
    var parts = content.split("#");
    var sub_parts;
    var tmp;
    for (var i = 0; i < parts.length; i++) {
        if(parts[i] != "") {
            sub_parts = parts[i].split("\n");
            var o = {
                "header" : sub_parts[0].trim(),
                "content" : [],
                "choices" : []
            };
            
            for (var j = 1; j < sub_parts.length; j++) {
                sub_parts[j] = sub_parts[j].trim();
            }
            
            for (var j = 1; j < sub_parts.length; j++) {
            
                tmp = sub_parts[j].indexOf(">");
                if (tmp == -1) {
                    if(sub_parts[j] != "") {
                        o.content.push(sub_parts[j]);
                    }
                } else {
                    o.choices.push(sub_parts[j]);
                }
            }
            CONTENT_PARSED.push(o);
        }
    }
}

function restoreSave(content) {
    if(!content.startsWith("SAVE")) {
        alert("Invalid or corrupted savefile!");
        return;
    }
    var parts = content.trim().split(">");
    if(parts[1] === "") {
        alert("Invalid or corrupted savefile!");
        return;
    } else {
        SAVE_HEADER = parts[1];
        document.getElementById("SaveLoaderIcon").style.boxShadow = "0px 0px 8px 8px #D4B037";
    }
    
}

function saveTextAsFile()
{
    var text = "SAVE>";
    text += CURRENT_LOC.header;
    
    
    var currentdate = new Date(); 
    var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + "_um_"  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes()


 
	var textToSave = text;
	var textToSaveAsBlob = new Blob([textToSave], {type:"text/plain"});
	var textToSaveAsURL = window.URL.createObjectURL(textToSaveAsBlob);
    
	var fileNameToSaveAs = "adventure_save_" + datetime + ".txt";
    
    
	var downloadLink = document.createElement("a");
	downloadLink.download = fileNameToSaveAs;
	downloadLink.innerHTML = "Download File";
	downloadLink.href = textToSaveAsURL;
    
	downloadLink.onclick = destroyClickedElement;
	downloadLink.style.display = "none";
    
	document.body.appendChild(downloadLink);
    
	downloadLink.click();
}

function destroyClickedElement(event)
{
	document.body.removeChild(event.target);
}

document.onkeypress = function(e) {
    e = e || window.event;
    var charCode = (typeof e.which == "number") ? e.which : e.keyCode;
    if (charCode) {
        var cont = String.fromCharCode(charCode)
        option(document.getElementById(cont),cont);
    }
}
