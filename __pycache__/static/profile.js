function fetchData() {
  fetch ('http://127.0.0.1:5000/users/we')
    .then(response => {
      console.log(response);
      if (!response.ok) {
        throw Error("ERROR");
      }
      return response.json();
  }).then(data => {
    console.log(data.data)
  }).catch(error => {
    console.log(error);
  });
}

fetchData();
