window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};


const deleteBtn = document.getElementById('delete-venue')

deleteBtn.onclick = (e) => {
    const venueId = e.target.dataset['id'];
    const deleted = true
    console.log("eeee", venueId)
    fetch('/venues/' + venueId + '/delete', {
      method: 'DELETE',
      body: JSON.stringify({
        'deleted' : deleted
      }),
      headers:({
        'Content-Type' : 'application/json'
      })
    })
    .then(function() {
      console.log("venue removed")
    })
    .catch(function(error) {
      console.log("error")
    })
}
