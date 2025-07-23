const video = document.getElementById('video');
const captureBtn = document.getElementById('capture-btn');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error('Camera permission denied:', err);
  });

captureBtn.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imageData = canvas.toDataURL('image/jpeg');

  fetch('/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imageData })
  }).then(res => {
    console.log('Image sent');
  }).catch(err => {
    console.error('Error uploading image:', err);
  });
});
