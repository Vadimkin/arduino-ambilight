var exec = require('child_process').exec,
	fs = require('fs'),
	PNG = require('pngjs').PNG,
	five = require("johnny-five"),
	LED = require('./models/led');

var filePath = fs.realpathSync(__dirname);

board = new five.Board();

diode = new LED(five, [5, 7, 6], 1);
diode2 = new LED(five, [10, 9, 8], 2);



board.on("ready", function() {
	setInterval(function() {
	     exec('screencapture -x screen.jpg', function (error, stdout, stderr) {

		fs.createReadStream(filePath + '/screen.jpg')
			.pipe(new PNG({
			  filterType: 4
			}))
			.on('parsed', function() {
				diode.updateColors(this.data, this.width, this.height);
				diode2.updateColors(this.data, this.width, this.height);
			})

	     });
	}, 10000);
});