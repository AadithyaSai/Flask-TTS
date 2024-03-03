const playPauseBtn = document.getElementById("play_pause_btn");
const micIcon = document.getElementById("mic_icon");
const audio = document.getElementById("audio");

audio.onended = () => {
  micIcon.classList.remove("playing");
};

playPauseBtn.onclick = () => {
  audio.play();
  micIcon.classList.add("playing");
};
