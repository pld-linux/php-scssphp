<?php
/**
 * Autoloader for php-scssphp and its' dependencies
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($classloader) || !($classloader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '/usr/share/php/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $classloader = new \Symfony\Component\ClassLoader\ClassLoader();
    $classloader->register();
}

$classloader->addPrefix('Leafo\\ScssPhp\\', dirname(dirname(__DIR__)));

return $classloader;
