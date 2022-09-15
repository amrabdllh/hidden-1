<!doctype html>
<html <?php language_attributes(); ?> class="<?php echo rentex_get_theme_option( 'site_mode' ) == 'dark' ? esc_attr( 'site-dark' ) : ''; ?>">
<head>
	<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-118240558-2"></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7148300905293580"
     crossorigin="anonymous"></script>	
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-118240558-2');
</script>
	<?php wp_head(); ?>

</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<?php do_action( 'rentex_before_site' ); ?>

<div id="page" class="hfeed site">
	<?php
	/**
	 * Functions hooked in to rentex_before_header action
	 *
	 *
	 */
	do_action( 'rentex_before_header' );

	get_template_part( 'template-parts/header/header', rentex_get_theme_option( 'header-type', 1 ) );

	/**
	 * Functions hooked in to rentex_before_content action
	 *
	 * @see rentex_breadcrumb - 10
	 *
	 */
	do_action( 'rentex_before_content' );
	?>

	<div id="content" class="site-content" tabindex="-1">
		<div class="col-full">

<?php
/**
 * Functions hooked in to rentex_content_top action
 *
 * @see rentex_shop_messages - 10 - woo
 */
do_action( 'rentex_content_top' );
