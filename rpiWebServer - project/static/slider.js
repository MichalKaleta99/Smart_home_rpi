const mySlider = document.getElementById("my-slider");
const sliderValue = document.getElementById("slider-value");
const mySlider2 = document.getElementById("my-slider2");
const sliderValue2 = document.getElementById("slider-value2");

function slider()
{
	valPercent = (mySlider.value / mySlider.max)*100;
    mySlider.style.background = `linear-gradient(to right, #3264fe ${valPercent}%, #d5d5d5 ${valPercent}%)`;
    sliderValue.textContent = mySlider.value;
}
slider();

function slider2()
{
	valPercent = (mySlider2.value / mySlider2.max)*100;
    mySlider2.style.background = `linear-gradient(to right, #FF0000 ${valPercent}%, #d5d5d5 ${valPercent}%)`;
    sliderValue2.textContent = mySlider2.value;
}
slider2();

