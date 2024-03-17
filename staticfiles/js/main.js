/**
 * scrollToTop
 * Header Fixed
 * mobileNav
 * ajaxContactForm
 * ajaxSubscribe
 * retinaLogos
 */

(function ($) {
  'use strict';

  // Scroll Top
  var scrollToTop = function () {
    $(window).scroll(function () {
      if ($(this).scrollTop() > 300) {
        $('#scroll-top').addClass('show');
      } else {
        $('#scroll-top').removeClass('show');
      }
    });

    $('#scroll-top').on('click', function () {
      $('html, body').animate({ scrollTop: 0 }, 'easeInOutExpo');
      return false;
    });
  };

  var headerFixed = function () {
    if ($('body').hasClass('header-fixed')) {
      var nav = $('#site-header');
      if (nav.length) {
        var offsetTop = nav.offset().top,
          injectSpace = $('<div />', {}).insertAfter(nav);
        $(window).on('load scroll', function () {
          if ($(window).scrollTop() > 300) {
            nav.addClass('is-fixed');
            injectSpace.show();
          } else {
            nav.removeClass('is-fixed');
            injectSpace.hide();
          }

          if ($(window).scrollTop() > 500) {
            nav.addClass('is-small');
          } else {
            nav.removeClass('is-small');
          }
        });
      }
    }
  };

  var mobileNav = function () {
    var mobile = window.matchMedia('(max-width: 991px)');
    var wrapMenu = $('#site-header .nav-wrap');
    var navExtw = $('.nav-extend.active');
    var navExt = $('.nav-extend.active').children();

    responsivemenu(mobile);

    mobile.addListener(responsivemenu);

    function responsivemenu(mobile) {
      if (mobile.matches) {
        // if media query matches

        $('#mainnav')
          .attr('id', 'mainnav-mobi')
          .appendTo('#site-header')
          .hide()
          .children('.menu')
          .append(navExt);
      } else {
        $('#mainnav-mobi')
          .attr('id', 'mainnav')
          .removeAttr('style')
          .prependTo(wrapMenu)
          .find('.ext')
          .appendTo(navExtw)
          .parent()
          .siblings('#mainnav');

        $('.btn-submenu').addClass('active');
        $('.btn-menu').removeClass('active');
        $('.sub-menu').css({ display: 'block' });
      }
    }

    $('.btn-menu').on('click', function () {
      $('#mainnav-mobi').slideToggle(300);
      $(this).toggleClass('active');
    });

    $(document).on('click', '#mainnav-mobi li .btn-submenu', function (e) {
      $(this).toggleClass('active').next('ul').slideToggle(300);
      e.stopImmediatePropagation();
    });
  };

  var ajaxContactForm = function () {
    $('#contactform').each(function () {
      $(this).validate({
        submitHandler: function (form) {
          var $form = $(form),
            str = $form.serialize(),
            loading = $('<div />', { class: 'loading' });

          $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: str,
            beforeSend: function () {
              $form.find('.form-submit').append(loading);
            },
            success: function (msg) {
              var result, cls;
              if (msg === 'Success') {
                result =
                  'Message Sent Successfully To Email Administrator. ( You can change the email management a very easy way to get the message of customers in the user manual )';
                cls = 'msg-success';
              } else {
                result = 'Error sending email.';
                cls = 'msg-error';
              }

              $form.prepend(
                $('<div />', {
                  class: 'flat-alert ' + cls,
                  text: result,
                }).append(
                  $('<a class="close" href="#"><i class="fa fa-close"></i></a>')
                )
              );

              $form.find(':input').not('.submit').val('');
            },
            complete: function (xhr, status, error_thrown) {
              $form.find('.loading').remove();
            },
          });
        },
      });
    }); // each contactform
  };

  var ajaxSubscribe = {
    obj: {
      subscribeEmail: $('#subscribe-email'),
      subscribeButton: $('#subscribe-button'),
      subscribeMsg: $('#subscribe-msg'),
      subscribeContent: $('#subscribe-content'),
      dataMailchimp: $('#subscribe-form').attr('data-mailchimp'),
      success_message:
        '<div class="notification_ok">Thank you for joining our mailing list! Please check your email for a confirmation link.</div>',
      failure_message:
        '<div class="notification_error">Error! <strong>There was a problem processing your submission.</strong></div>',
      noticeError: '<div class="notification_error">{msg}</div>',
      noticeInfo: '<div class="notification_error">{msg}</div>',
      basicAction: 'mail/subscribe.php',
      mailChimpAction: 'mail/subscribe-mailchimp.php',
    },

    eventLoad: function () {
      var objUse = ajaxSubscribe.obj;

      $(objUse.subscribeButton).on('click', function () {
        if (window.ajaxCalling) return;
        var isMailchimp = objUse.dataMailchimp === 'true';

        if (isMailchimp) {
          ajaxSubscribe.ajaxCall(objUse.mailChimpAction);
        } else {
          ajaxSubscribe.ajaxCall(objUse.basicAction);
        }
      });
    },

    ajaxCall: function (action) {
      window.ajaxCalling = true;
      var objUse = ajaxSubscribe.obj;
      var messageDiv = objUse.subscribeMsg.html('').hide();
      $.ajax({
        url: action,
        type: 'POST',
        dataType: 'json',
        data: {
          subscribeEmail: objUse.subscribeEmail.val(),
        },
        success: function (responseData, textStatus, jqXHR) {
          if (responseData.status) {
            objUse.subscribeContent.fadeOut(500, function () {
              messageDiv.html(objUse.success_message).fadeIn(500);
            });
          } else {
            switch (responseData.msg) {
              case 'email-required':
                messageDiv.html(
                  objUse.noticeError.replace(
                    '{msg}',
                    'Error! <strong>Email is required.</strong>'
                  )
                );
                break;
              case 'email-err':
                messageDiv.html(
                  objUse.noticeError.replace(
                    '{msg}',
                    'Error! <strong>Email invalid.</strong>'
                  )
                );
                break;
              case 'duplicate':
                messageDiv.html(
                  objUse.noticeError.replace(
                    '{msg}',
                    'Error! <strong>Email is duplicate.</strong>'
                  )
                );
                break;
              case 'filewrite':
                messageDiv.html(
                  objUse.noticeInfo.replace(
                    '{msg}',
                    'Error! <strong>Mail list file is open.</strong>'
                  )
                );
                break;
              case 'undefined':
                messageDiv.html(
                  objUse.noticeInfo.replace(
                    '{msg}',
                    'Error! <strong>undefined error.</strong>'
                  )
                );
                break;
              case 'api-error':
                objUse.subscribeContent.fadeOut(500, function () {
                  messageDiv.html(objUse.failure_message);
                });
            }
            messageDiv.fadeIn(500);
          }
        },
        error: function (jqXHR, textStatus, errorThrown) {
          alert('Connection error');
        },
        complete: function (data) {
          window.ajaxCalling = false;
        },
      });
    },
  };

  var retinaLogos = function () {
    var retina = window.devicePixelRatio > 1 ? true : false;
    if (retina) {
      $('.logo').find('img').attr({ src: 'assets/image/logo@2x.png' });
    }
  };

  $(function () {
    scrollToTop();
    headerFixed();
    mobileNav();
    ajaxContactForm();
    $(window).on('load resize', function () {
      retinaLogos();
    });
  });
})(jQuery);
