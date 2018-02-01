$(document).ready(function() {
  $('#endpoint_sip-host').on('change', function (e) {
    toggle_endpoint_sip_host_mode.call(this)
  })
  toggle_endpoint_sip_host_mode.call($('#endpoint_sip-host'))
  $('#endpoint_iax-host').on('change', function (e) {
    toggle_endpoint_iax_host_mode.call(this)
  })
  toggle_endpoint_iax_host_mode.call($('#endpoint_iax-host'))
});


function toggle_endpoint_sip_host_mode() {
  if ($(this).val() == 'dynamic') {
    $('#endpoint_sip-host_value').closest('div.form-group').hide()
  } else {
    $('#endpoint_sip-host_value').closest('div.form-group').show()
  }
}


function toggle_endpoint_iax_host_mode() {
  if ($(this).val() == 'dynamic') {
    $('#endpoint_iax-host_value').closest('div.form-group').hide()
  } else {
    $('#endpoint_iax-host_value').closest('div.form-group').show()
  }
}