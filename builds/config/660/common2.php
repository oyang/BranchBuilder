<?php
// static vars that are used in multiple scripts
require_once( "common.php" );

global $MAIL_BUILD_TO;
global $ON_DEMAND;
global $PUBLISH;
global $DEPLOY;
global $QATEST;
global $BUILD_BRANCH;

if($MAIL_BUILD_TO == '') $MAIL_BUILD_TO  = "";
if($ON_DEMAND == '')  	 $ON_DEMAND      = false;
if($PUBLISH == '') 	 $PUBLISH        = false;
if($DEPLOY == '')	 $DEPLOY         = false;
if($QATEST == '')	 $QATEST         = false;
$SRC_DIR        = "sugarcrm";
$MOD_DIR        = "sugarmods";
#$BUILD_DIR      = "build";
$TMP_DIR        = "tmp";
$ZIP_DIR        = "zip";
$ZIP_CMD        = "zip -q -9";
$RC             = 0;    # return code

$BASE_BUILD_DIR = "/dev/shm/sugarbuild-$VER_SUFFIX";
$ROME_BUILD_DIR ="build/rome/builds";

$LOG_FILE       = "build-log.txt";
$DEPLOY_LOG_FILE = $BASE_BUILD_DIR . "/deploy-log.txt";

if($BUILD_BRANCH){
	$VER_SUFFIX_TMP_3 = $BUILD_BRANCH;
}else {
	$VER_SUFFIX_TMP_3 = $VER_SUFFIX;
}
$CE_BASE_DIR    = "SugarCE-$VER_SUFFIX_TMP_3";
$CE_DIR         = "SugarCE-Full-$VER_SUFFIX_TMP_3";
$CE_PATCH       = "SugarCE-Patch-$VER_SUFFIX_TMP_3";

$EXP_BASE_DIR    = "SugarExpress-$VER_SUFFIX_TMP_3";
$EXP_DIR         = "SugarExpress-Full-$VER_SUFFIX_TMP_3";
$EXP_PATCH       = "SugarExpress-Patch-$VER_SUFFIX_TMP_3";

$SALES_BASE_DIR    = "SugarSales-$VER_SUFFIX_TMP_3";
$SALES_DIR         = "SugarSales-Full-$VER_SUFFIX_TMP_3";
$SALES_PATCH       = "SugarSales-Patch-$VER_SUFFIX_TMP_3";

$ULT_BASE_DIR   = "SugarUlt-$VER_SUFFIX_TMP_3";
$ULT_DIR        = "SugarUlt-Full-$VER_SUFFIX_TMP_3";
$ULT_PATCH      = "SugarUlt-Patch-$VER_SUFFIX_TMP_3";
$ULT_OD_BASE_DIR   = "SugarUlt-OD-$VER_SUFFIX_TMP_3";
$ULT_OD_DIR        = "SugarUlt-OD-Full-$VER_SUFFIX_TMP_3";

$ENT_BASE_DIR   = "SugarEnt-$VER_SUFFIX_TMP_3";
$ENT_DIR        = "SugarEnt-Full-$VER_SUFFIX_TMP_3";
$ENT_PATCH      = "SugarEnt-Patch-$VER_SUFFIX_TMP_3";
$ENT_OD_BASE_DIR   = "SugarEnt-OD-$VER_SUFFIX_TMP_3";
$ENT_OD_DIR        = "SugarEnt-OD-Full-$VER_SUFFIX_TMP_3";

$CORP_BASE_DIR   = "SugarCorp-$VER_SUFFIX_TMP_3";
$CORP_DIR        = "SugarCorp-Full-$VER_SUFFIX_TMP_3";
$CORP_PATCH      = "SugarCorp-Patch-$VER_SUFFIX_TMP_3";
$CORP_OD_BASE_DIR   = "SugarCorp-OD-$VER_SUFFIX_TMP_3";
$CORP_OD_DIR        = "SugarCorp-OD-Full-$VER_SUFFIX_TMP_3";

$PRO_BASE_DIR   = "SugarPro-$VER_SUFFIX_TMP_3";
$PRO_DIR        = "SugarPro-Full-$VER_SUFFIX_TMP_3";
$PRO_PATCH      = "SugarPro-Patch-$VER_SUFFIX_TMP_3";
$PRO_OD_BASE_DIR   = "SugarPro-OD-$VER_SUFFIX_TMP_3";
$PRO_OD_DIR        = "SugarPro-OD-Full-$VER_SUFFIX_TMP_3";

$DCE_BASE_DIR   = "SugarDCE-$VER_SUFFIX_TMP_3";
$DCE_DIR        = "SugarDCE-Full-$VER_SUFFIX_TMP_3";

$DEV_BASE_DIR   = "SugarDevEdition-$VER_SUFFIX_TMP_3";
$DEV_DIR        = "SugarDevEdition-Full-$VER_SUFFIX_TMP_3";
/*No developer patch yet*/
//$DEV_PATCH    = "SugarDevEdition-Patch-$VER_SUFFIX";


$OLD_VER_SUFFIX_1 = "5.5.1";
$OLD_CE_ZIP_1     = "/home/public/sugar_release_archive/ce/SugarCE-" . $OLD_VER_SUFFIX_1 . ".zip";
$OLD_EXP_ZIP_1     = "/home/public/sugar_release_archive/express/SugarExpress-". $OLD_VER_SUFFIX_1 . ".zip";
$OLD_PRO_ZIP_1    = "/home/public/sugar_release_archive/pro/SugarPro-"  . $OLD_VER_SUFFIX_1 . ".zip";
$OLD_ENT_ZIP_1    = "/home/public/sugar_release_archive/ent/SugarEnt-"  . $OLD_VER_SUFFIX_1 . ".zip";

$OLD_VER_SUFFIX_2 = "6.0.x";
$OLD_VER_SUFFIX_2_PACKAGE = "6.0.0";
$OLD_CE_ZIP_2     = "/home/public/sugar_release_archive/ce/SugarCE-" . $OLD_VER_SUFFIX_2_PACKAGE . ".zip";
$OLD_EXP_ZIP_2     = "/home/public/sugar_release_archive/express/SugarExpress-".  $OLD_VER_SUFFIX_2_PACKAGE . ".zip";
$OLD_PRO_ZIP_2    = "/home/public/sugar_release_archive/pro/SugarPro-"  . $OLD_VER_SUFFIX_2_PACKAGE . ".zip";
$OLD_ENT_ZIP_2    = "/home/public/sugar_release_archive/ent/SugarEnt-"  . $OLD_VER_SUFFIX_2_PACKAGE . ".zip";

$OLD_VER_SUFFIX_3 = "6.1.x";
$OLD_VER_SUFFIX_3_PACKAGE = "6.1.0RC1";
$OLD_CE_ZIP_3     = "/home/public/sugar_release_archive/ce/SugarCE-" . $OLD_VER_SUFFIX_3_PACKAGE . ".zip";
$OLD_EXP_ZIP_3     = "/home/public/sugar_release_archive/express/SugarExpress-".  $OLD_VER_SUFFIX_3_PACKAGE . ".zip";
$OLD_PRO_ZIP_3    = "/home/public/sugar_release_archive/pro/SugarPro-"  . $OLD_VER_SUFFIX_3_PACKAGE . ".zip";
$OLD_ENT_ZIP_3    = "/home/public/sugar_release_archive/ent/SugarEnt-"  . $OLD_VER_SUFFIX_3_PACKAGE . ".zip";

$GA_VER_SUFFIX = $VER_SUFFIX;
$GA_CE_ZIP     = "/home/public/sugar_release_archive/ce/SugarCE-" . $GA_VER_SUFFIX . ".zip";
$GA_EXP_ZIP     = "/home/public/sugar_release_archive/express/SugarExpress-" . $GA_VER_SUFFIX . ".zip";
$GA_PRO_ZIP    = "/home/public/sugar_release_archive/pro/SugarPro-"  . $GA_VER_SUFFIX . ".zip";
$GA_ENT_ZIP    = "/home/public/sugar_release_archive/ent/SugarEnt-"  . $GA_VER_SUFFIX . ".zip";

$CE_UPGRADE_1   = "SugarCE-Upgrade-$OLD_VER_SUFFIX_1-to-$VER_SUFFIX";
$EXP_UPGRADE_1  = "SugarExpress-Upgrade--$OLD_VER_SUFFIX_1-to-$VER_SUFFIX";
$PRO_UPGRADE_1  = "SugarPro-Upgrade-$OLD_VER_SUFFIX_1-to-$VER_SUFFIX";
$ENT_UPGRADE_1  = "SugarEnt-Upgrade-$OLD_VER_SUFFIX_1-to-$VER_SUFFIX";

$CE_UPGRADE_2   = "SugarCE-Upgrade-$OLD_VER_SUFFIX_2-to-$VER_SUFFIX";
$EXP_UPGRADE_2  = "SugarExpress-Upgrade-$OLD_VER_SUFFIX_2-to-$VER_SUFFIX";
$PRO_UPGRADE_2  = "SugarPro-Upgrade-$OLD_VER_SUFFIX_2-to-$VER_SUFFIX";
$ENT_UPGRADE_2  = "SugarEnt-Upgrade-$OLD_VER_SUFFIX_2-to-$VER_SUFFIX";

$CE_UPGRADE_3   = "SugarCE-Upgrade-$OLD_VER_SUFFIX_3-to-$VER_SUFFIX";
$EXP_UPGRADE_3  = "SugarExpress-Upgrade-$OLD_VER_SUFFIX_3-to-$VER_SUFFIX";
$PRO_UPGRADE_3  = "SugarPro-Upgrade-$OLD_VER_SUFFIX_3-to-$VER_SUFFIX";
$ENT_UPGRADE_3  = "SugarEnt-Upgrade-$OLD_VER_SUFFIX_3-to-$VER_SUFFIX";


$CE_TO_PRO_CONVERSION = "SugarCE-to-SugarPro-Conversion-$VER_SUFFIX";
$CE_TO_ENT_CONVERSION = "SugarCE-to-SugarEnt-Conversion-$VER_SUFFIX";
$PRO_TO_ENT_CONVERSION = "SugarPro-to-SugarEnt-Conversion-$VER_SUFFIX";
?>
