<<<<<<< HEAD
import crypto from "crypto";

const args = process.argv.slice(2);

const student = args[0];
const score = args[1];

const record = {
    student: student,
    score: score,
    timestamp: Date.now()
};

const hash = crypto
    .createHash("sha256")
    .update(JSON.stringify(record))
    .digest("hex");

=======
import crypto from "crypto";

const args = process.argv.slice(2);

const student = args[0];
const score = args[1];

const record = {
    student: student,
    score: score,
    timestamp: Date.now()
};

const hash = crypto
    .createHash("sha256")
    .update(JSON.stringify(record))
    .digest("hex");

>>>>>>> 4af0533a6ff38f39f444806c9ed2167a1f080f88
console.log(hash);