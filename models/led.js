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

	stepR = (this.oldColors['r'] - this.currentColors['r']) / 101;
	stepG = (this.oldColors['g'] - this.currentColors['g']) / 101;
	stepB = (this.oldColors['b'] - this.currentColors['b']) / 101;


	for(var i = 0; i <= 100; i++) {
		var led = this;
		(function(i) {
			setTimeout(function() {
				r = (led.oldColors['r'] - stepR * i).toFixed(0);
				g = (led.oldColors['g'] - stepG * i).toFixed(0);
				b = (led.oldColors['b'] - stepB * i).toFixed(0);
				led.pins.color(led.rgbToHex(r, g, b));
			}, i * 10);
		})(i);
	}
}

LED.prototype.rgbToHex = function(r, g, b) {
    return this.toHex(r)+this.toHex(g)+this.toHex(b);
}

LED.prototype.toHex = function(n) {
	n = parseInt(n,10);
	if (isNaN(n)) return "00";
	n = Math.max(0,Math.min(n,255));
	return "0123456789ABCDEF".charAt((n-n%16)/16)
	  + "0123456789ABCDEF".charAt(n%16);
}

module.exports = LED;