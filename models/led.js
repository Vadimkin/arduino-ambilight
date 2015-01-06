var LED = function(five, pins, position) {
	// Pins
	this.pins = pins

	// Creator ID
	this.currentColors = {'r': 0, 'g': 0, 'b': 0};

	// Objects IDs of players
	this.oldColors = {'r': 0, 'g': 0, 'b': 0};

	// Position. 1 — left, 2 — right
	this.position = position;

	// Board
	this.five = five;
}

LED.prototype.updateColors = function(data, width, height){
	this.oldColors['r'] = this.currentColors['r'];
	this.oldColors['g'] = this.currentColors['g'];
	this.oldColors['b'] = this.currentColors['b'];

	var heightCenter = height/2;

	switch(this.position) {
		case 1: {
			this.currentColors['r'] = data[(width * heightCenter + 0) << 2];
			this.currentColors['g'] = data[((width * heightCenter + 0) << 2) + 1];
			this.currentColors['b'] = data[((width * heightCenter + 0) << 2) + 2];
			break;
		}
		case 2: {
			this.currentColors['r'] = data[(width * heightCenter + (width - 1)) << 2];
			this.currentColors['g'] = data[((width * heightCenter + (width - 1)) << 2) + 1];
			this.currentColors['b'] = data[((width * heightCenter + (width - 1)) << 2) + 2];
			break;
		}
	}

	// this.oldColors['r'] = 0;
	// this.oldColors['g'] = 0;
	// this.oldColors['b'] = 0;

	// this.currentColors['r'] = 255;
	// this.currentColors['g'] = 255;
	// this.currentColors['b'] = 255;

	stepR = (this.oldColors['r'] - this.currentColors['r']) / 100;
	stepG = (this.oldColors['g'] - this.currentColors['g']) / 100;
	stepB = (this.oldColors['b'] - this.currentColors['b']) / 100;

	for(var i = 0; i <= 100; i++) {
		var led = this;
		(function(i) {
			setTimeout(function() {
				led.draw(led.pins[0], led.oldColors['r'] - stepR * i);
				led.draw(led.pins[1], led.oldColors['g'] - stepG * i);
				led.draw(led.pins[2], led.oldColors['b'] - stepB * i);
			}, i * 10);
		})(i);
	}
}

LED.prototype.draw = function(pin, value) {
	this.five.Led(pin).brightness(value);
}

module.exports = LED;