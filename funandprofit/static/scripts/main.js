var pluralize = function (word, count) {
  if (count === 1) { return word; }

  return word + 's';
};

var bulkSelectors = {
  'selectAll': '#select_all',
  'checkedItems': '.checkbox-item',
  'colheader': '.col-header',
  'selectedRow': 'warning',
  'updateScope': '#scope',
  'bulkActions': '#bulk_actions'
};

$(document).ready(function() {

setInterval(function() {$("#div1").load("portal/scenario");}, 20000);

setInterval(function() {$("#div2").load("portal/supplement");}, 20000);

//setInterval(function() {
//      $.getJSON("portal/refreshmoney",
//              function(data) {
//                  $('#userMoney').text(data.user_money);
//              });
//}, 10000);
  
  // Date formatting with momentjs.
  $('.from-now').each(function (i, e) {
    (function updateTime() {
      var time = moment($(e).data('datetime'));
      $(e).text(time.fromNow());
      $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
      setTimeout(updateTime, 1000);
    })();
  });

  $('.short-date').each(function (i, e) {
    var time = moment($(e).data('datetime'));
    $(e).text(time.format('MMM Do YYYY'));
    $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
  });
  
  // Bulk delete.
  $('body').on('change', bulkSelectors.checkedItems, function () {
    var checkedSelector = bulkSelectors.checkedItems + ':checked';
    var itemCount = $(checkedSelector).length;
    var pluralizeItem = pluralize('item', itemCount);
    var scopeOptionText = itemCount + ' selected ' + pluralizeItem;

    if ($(this).is(':checked')) {
      $(this).closest('tr').addClass(bulkSelectors.selectedRow);

      $(bulkSelectors.colheader).hide();
      $(bulkSelectors.bulkActions).show();
    }
    else {
      $(this).closest('tr').removeClass(bulkSelectors.selectedRow);

      if (itemCount === 0) {
        $(bulkSelectors.bulkActions).hide();
        $(bulkSelectors.colheader).show();
      }
    }

    $(bulkSelectors.updateScope + ' option:first').text(scopeOptionText);
  });

  $('body').on('change', bulkSelectors.selectAll, function () {
    var checkedStatus = this.checked;

    $(bulkSelectors.checkedItems).each(function () {
      $(this).prop('checked', checkedStatus);
      $(this).trigger('change');
    });
  });

  $('.helpButton').on('click', function() {
    req = $.ajax({
        url : '/portal/help',
        type : 'POST',
    });

    req.done(function(data) {
        $('#moneySection').fadeOut(1000).fadeIn(1000);
        $('#userMoney').text(data.user_money);
        alert("Help is on the way. $5 has been deducted from your account. Do not click the 'HELP' button again until help arrives.");
      });
  });

  $('.finishButton').on('click', function() {
    reqFinish = $.ajax({
        url : '/portal/finish',
        type : 'POST',
    });

    reqFinish.done(function() {
        alert("A proctor is queued up to check your work. Sit back, relax, and wait.");
    });
  });
});