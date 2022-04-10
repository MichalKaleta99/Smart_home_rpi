class PinLogin 
{
	constructor ({el, maxNumbers = 4}) 
	{
		this.el = 
		{
            main: el,
            numPad: el.querySelector(".pin-login__numpad"),
            textDisplay: el.querySelector(".pin-login__text")
        };

        this.maxNumbers = maxNumbers;
        this.value = "";
        this._generatePad();
    }

    _generatePad() 
	{
        const padLayout = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "backspace", "0", "done"
        ];

        padLayout.forEach(key => 
		{
            const insertBreak = key.search(/[369]/) !== -1;
            const keyEl = document.createElement("div");

            keyEl.classList.add("pin-login__key");
            keyEl.classList.toggle("material-icons", isNaN(key));
            keyEl.textContent = key;
            keyEl.addEventListener("click", () => { this._handleKeyPress(key) });
            this.el.numPad.appendChild(keyEl);

            if (insertBreak) 
			{
                this.el.numPad.appendChild(document.createElement("br"));
            }
        });
    }

    _handleKeyPress(key) 
	{
        switch (key) 
		{
            case "backspace":
                this.value = this.value.substring(0, this.value.length - 1);
                break;
            case "done":
                this._attemptLogin();
                break;
            default:
                if (this.value.length < this.maxNumbers) 
				{
                    this.value += key;
                }
                break;
        }
        this._updateValueText();
    }

    _updateValueText()
	{
        this.el.textDisplay.value = this.value;
    }

    _attemptLogin()
	{
		if (this.value === "1234")
		{
			window.location.replace("/templates/door_on");
		} 
		else 
		{				
		    alert("Nieprawidłowy PIN! Spróbuj ponownie.");
		    window.location.replace("/templates/door_alert");
		}
    }
}

new PinLogin(
{
    el: document.getElementById("mainPinLogin"),
});
