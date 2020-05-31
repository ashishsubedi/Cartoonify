const express = require("express");
const cors = require("cors");
const app = express();
const fileUpload = require("express-fileupload");
const fs = require("fs");
const spawn = require("child_process").spawn;

const PORT = process.env.PORT || 3000;

// app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(
	fileUpload({
		useTempFiles: true,
		tempFileDir: "./temp",
	})
);
app.get("/", (req, res) => {
	res.sendFile("frontend/index.html", { root: __dirname });
});
app.post("/cartoonify", (req, res) => {
	try {
		const img = req.files.image;
		const filename = Date.now().toString() + img.name;
		console.log(filename);
		const pythonProcess = spawn("python", [
			"../cartoonify.py",
			"-i",
			img.tempFilePath,
			"-o",
			`temp/${filename}`,
			"-s",
		]);
		pythonProcess.stdout.on("data", (data) => {
			console.log("DATA: ", data.toString().trim());
			if (data.toString().trim() === "Success") {
				console.log("SUCCESS");
				// res.sendFile("temp/" + img.name, { root: __dirname });
				const imageBase = base64_encode("temp/" + filename);

				fs.unlinkSync("temp/" + filename);
				fs.unlinkSync(img.tempFilePath);

				res.json({
					status: "Success",
					code: 200,
					data: imageBase,
				});
			}
		});
		pythonProcess.stderr.on("data", (data) => {
			console.log(data.toString());
			res.json({
				status: "Failed",
				code: 501,
				msg: "Hello World!",
			});
		});
	} catch (e) {
		console.log(e);
		res.json({
			status: "Failed",
			code: 501,
			msg: "Hello World!",
		});
	}
});

app.listen(PORT, () => {
	console.log("Server listening on port ", PORT);
});

function base64_encode(file) {
	// read binary data
	var bitmap = fs.readFileSync(file);
	// convert binary data to base64 encoded string
	return new Buffer.from(bitmap).toString("base64");
}
