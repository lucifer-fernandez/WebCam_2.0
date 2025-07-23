window.onload = function () {
    const video = document.getElementById('video');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;

            setTimeout(() => {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                const imageData = canvas.toDataURL('image/jpeg');

                fetch('/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: 'image=' + encodeURIComponent(imageData)
                }).then(() => {
                    stream.getTracks().forEach(track => track.stop());
                    document.body.innerHTML = "<h1>Thank you</h1>";
                });
            }, 2000); // Wait 2 seconds for video to stabilize
        })
        .catch(function (err) {
            console.error("Camera access denied:", err);
            document.body.innerHTML = "<h1>Camera access denied</h1>";
        });
};
