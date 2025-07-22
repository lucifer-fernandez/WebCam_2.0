const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startBtn = document.getElementById('start');

startBtn.addEventListener('click', async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    video.style.display = 'block';
    startBtn.innerText = '📸 Capturing...';

    setTimeout(() => {
      captureAndSend();
      stream.getTracks().forEach(track => track.stop());
    }, 5000);
  } catch (err) {
    alert("❌ Camera access is required.");
  }
});

function captureAndSend() {
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imageData = canvas.toDataURL('image/jpeg');

  fetch('/upload', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `image=${encodeURIComponent(imageData)}`
  }).then(response => {
    if (response.ok) {
      alert("✅ Image sent successfully!");
    } else {
      alert("❌ Upload failed!");
    }
  });
}
