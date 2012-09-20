<?php
// 6.4.x and 6.5.x means upgrade package can be applied which version
// 6.4.0 and 6.5.0 means based on sugar version
// For building silent script, you have to building CE and Pro flavor installer package firstly
$UPGRADE_PACKAGES = array(
    "Upgrades" => array(
		"6.4.x" => array(
			"BASE_VERSION" => "6.4.0",
			"PACKAGE_LIST" => array( "Ult", "Corp", "Ent", "Pro", "CE" ),
			),
		"6.5.x" => array(
			"BASE_VERSION" => "6.5.0",
			"PACKAGE_LIST" => array( "Ult", "Corp", "Ent", "Pro", "CE" ),
			),
      ),
     "Conversions" => array(
       "CE_TO_PRO" => "SugarCE-to-SugarPro-Conversion",
       "CE_TO_ENT" => "SugarCE-to-SugarEnt-Conversion",
       "PRO_TO_ENT" => "SugarPro-to-SugarEnt-Conversion",
       "CE_TO_CORP" => "SugarCE-to-SugarCorp-Conversion",
       "CE_TO_ULT" => "SugarCE-to-SugarUlt-Conversion",
       "PRO_TO_CORP" => "SugarPro-to-SugarCorp-Conversion",
       "PRO_TO_ULT" => "SugarPro-to-SugarUlt-Conversion",
       "CORP_TO_ENT" => "SugarCorp-to-SugarEnt-Conversion",
       "CORP_TO_ULT" => "SugarCorp-to-SugarUlt-Conversion",
       "ENT_TO_ULT" => "SugarEnt-to-SugarUlt-Conversion",
     ),
     "SilentScript" => true,
);
?>
