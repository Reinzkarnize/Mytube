// document.addEventListener('DOMContentLoaded', function() {
    var remove_btn = document.querySelector(".fa-trash");
    var removeButtons = document.querySelectorAll('.remove_playlist');
    var playlistLinks = document.querySelectorAll('.playlist_link');
    var isOpen2 = false;

    function toggleMenu() {
      isOpen2 = !isOpen2;

      removeButtons.forEach((removeButton) => {
        removeButton.style.display = isOpen2 ? "flex" : "none";
      });

      playlistLinks.forEach((playlistLink) => {
        playlistLink.style.display = isOpen2 ? "none" : "block";
      });

      remove_btn.style.color = isOpen2? "red": "white";
    }

    remove_btn.addEventListener('click', toggleMenu);
  // });
