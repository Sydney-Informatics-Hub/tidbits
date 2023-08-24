$(document).ready(function () {
  $("#tipue_search_input").tipuesearch({
    mode: "json",
    show: 10,
    newWindow: false,
    contentLocation: "{{ SITEURL }}/tipuesearch_content.json",
  });
});
