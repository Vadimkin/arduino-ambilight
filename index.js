var exec = require('child_process').exec,
	fs = require('fs'),
	PNG = require('pngjs').PNG,
	five = require("johnny-five"),
	LED = require('./models/led');

var filePath = fs.realpathSync(__dirname);

board = new five.Board();


board.on("ready", function() {

	diode = new LED(five, five.Led.RGB([5, 7, 6]), 1);
	diode2 = new LED(five, five.Led.RGB([10, 9, 8]), 2);

	setInterval(function() {
	    exec('screencapture -x screen.jpg', function (error, stdout, stderr) {

		fs.createReadStream(filePath + '/screen.jpg')
			.pipe(new PNG({
			  filterType: 4
			}))
			.on('parsed', function() {
				diode2.updateColors(this.data, this.width, this.height);
				diode.updateColors(this.data, this.width, this.height);
			})

	    });
	}, 2000);
});