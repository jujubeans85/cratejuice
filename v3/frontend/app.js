// CHANGE THESE TO ANY URLs YOU WANT
const TRACK_1 = "https://filesamples.com/samples/audio/mp3/sample3.mp3";
const TRACK_2 = "https://filesamples.com/samples/audio/mp3/sample4.mp3";

function playTrack(num) {
  const player = document.getElementById("player");
  player.src = num === 1 ? TRACK_1 : TRACK_2;
  player.play();
}
