document.getElementById("txt_1").value = getSavedValue("txt_1");
document.getElementById("txt_2").value = getSavedValue("txt_2");
document.getElementById("txt_3").value = getSavedValue("txt_3");
document.getElementById("txt_4").value = getSavedValue("txt_4");
document.getElementById("my-slider").value = getSavedValue("my-slider"); 
document.getElementById("my-slider2").value = getSavedValue("my-slider2"); 
document.getElementById("slider-value").value = getSavedValue("slider-value");
document.getElementById("slider-value2").value = getSavedValue("slider-value2");

function saveValue(e)
{
    var id = e.id; 
    var val = e.value;
    localStorage.setItem(id, val);
}

function getSavedValue(v)
{
	if (!localStorage.getItem(v)) 
	{
		return "";
    }
	return localStorage.getItem(v);
}