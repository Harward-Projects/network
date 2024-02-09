// document.addEventListener('DOMContentLoaded', function () {
//   // Use links to toggle between views
// });

// This section grabs visible editPost_id's buttons and performs edit by means of fetch method (POST) and Django edit_post function
// The url get path for edit_post function most be considered for security and/or clean code to be unreachable
const editPostButton = document.querySelectorAll('[id^="editPost_"]');
editPostButton.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default button action

    const buttonId = button.id; // Get the button's id ("editPost_<post.id>")
    const postId = buttonId.split('_')[1]; // Split the id string and get the second part (post.id)
    console.log('Button clicked', buttonId);
    console.log('Post ID:', postId);

    const csrftoken = document.querySelector(
      '[name=csrfmiddlewaretoken]'
    ).value;
    fetch(`/post/${postId}/edit/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        // Any data you need to send to the server...
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to update the post.');
        }
        // Handle successful response...
      })
      .catch((error) => {
        console.error('Error updating the post:', error);
      });
  });
});

// This section grabs visible likeIcon_id's spans and performs front and back manipulation for
// like/unlike by means of fetch method (PUT) and Django like_unlike_post function
const likeIconForPost = document.querySelectorAll('[id^="likeIconForPost_"]');
likeIconForPost.forEach((likeIcon) => {
  // likeIcon.addEventListener('click', (event) => {
  // event.preventDefault(); // Prevent the default icon action
  // Toggles between Red and Gray just in front
  likeIcon.addEventListener('click', () => {
    // This if statement is to tackle authentication recognition status from the new post.
    if (document.getElementById('newPostId')) {
      console.log('User is logged in');
      if (likeIcon.style.color != 'red') {
        likeIcon.style.color = 'red';
      } else {
        likeIcon.style.color = '#818a91';
      }
      const likeIconId = likeIcon.id; // Get the likeIcon's id ("likeIconForPost_<post.id>")
      const postId = likeIconId.split('_')[1]; // Split the id string and get the second part (post.id)
      const likeCountId = `likeCountForPost_${postId}`;
      console.log('LikeIcon clicked', likeIconId);
      console.log('Post ID:', postId);
      console.log('Like count:', likeCountId);
      likeCountElement = document.getElementById(likeCountId);

      const csrftoken = document.querySelector(
        '[name=csrfmiddlewaretoken]'
      ).value;
      fetch(`/post/${postId}/like/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
          liked: likeIcon.style.color === 'red', // Determine liked based on the color
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to update post like/unlike state.');
          }
          return response.json();
        })
        .then((data) => {
          likeCountElement.textContent = data.like_count;
        })
        .catch((error) => {
          console.error('Error updating post like/unlike state:', error);
        });
    } else {
      alert('Please log in to perform this action.');
    }
  });
});
