#!/bin/bash

echo 'Thanks for playing PZ! This script brought to you by Rathlord!'

cd "$(dirname "$0")"

jre/Contents/Home/bin/java \
    -Djava.awt.headless=true -XstartOnFirstThread \
    -Djava.library.path=natives/:. \
    -Xmx24g \
    -Duser.home=/Users/benjaminmarchand/temp \
    -Dzomboid.steam=1 -Dzomboid.znetlog=1 \
    -classpath java/istack-commons-runtime.jar;java/jassimp.jar;java/javacord-2.0.17-shaded.jar;java/javax.activation-api.jar;java/jaxb-api.jar;java/jaxb-runtime.jar;java/jinput.jar;java/lwjgl.jar;java/lwjgl-natives-macos.jar;java/lwjgl-glfw.jar;java/lwjgl-glfw-natives-macos.jar;java/lwjgl-jemalloc.jar;java/lwjgl-jemalloc-natives-macos.jar;java/lwjgl-opengl.jar;java/lwjgl-opengl-natives-macos.jar;java/lwjgl_util.jar;java/sqlite-jdbc-3.27.2.1.jar;java/trove-3.0.3.jar;java/uncommons-maths-1.2.3.jar;java/ \
    zombie/network/GameServer