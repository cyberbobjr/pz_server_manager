#!/bin/bash

# Initial configuration and necessary variable retrieval
EXE_PATH="<path_to_java.exe_folder>" # Replace <path_to_java.exe_folder> with the actual path
MEMORY="<memory_size>" # Replace <memory_size> with the allocated memory size, in GB
SERVER_PATH="<server_folder_path>" # Replace <server_folder_path> with the actual path
SERVER_ADMIN_PASSWORD="<admin_password>" # Replace <admin_password> with the server's admin password

# Java command
JAVA_COMMAND="$EXE_PATH/jre64/bin/java"

# Java options
JAVA_OPTIONS="-Djava.awt.headless=true -Dzomboid.steam=1 \
-Dzomboid.znetlog=1 -XX:+UseZGC -XX:-CreateCoredumpOnCrash \
-XX:-OmitStackTraceInFastThrow -Xms${MEMORY}g -Xmx${MEMORY}g \
-Djava.library.path=natives/:natives/win64/:. -Duser.home=\"${SERVER_PATH}\""

# Classpath
CLASSPATH="-cp java/istack-commons-runtime.jar:java/jassimp.jar:\
java/javacord-2.0.17-shaded.jar:java/javax.activation-api.jar:\
java/jaxb-api.jar:java/jaxb-runtime.jar:java/lwjgl.jar:\
java/lwjgl-natives-windows.jar:java/lwjgl-glfw.jar:\
java/lwjgl-glfw-natives-windows.jar:java/lwjgl-jemalloc.jar:\
java/lwjgl-jemalloc-natives-windows.jar:java/lwjgl-opengl.jar:\
java/lwjgl-opengl-natives-windows.jar:java/lwjgl_util.jar:\
java/sqlite-jdbc-3.27.2.1.jar:java/trove-3.0.3.jar:\
java/uncommons-maths-1.2.3.jar:java/commons-compress-1.18.jar:java/"

# Main class to execute
MAIN_CLASS="zombie.network.GameServer"

# Additional arguments
ADDITIONAL_ARGS="-statistic 0 -adminpassword ${SERVER_ADMIN_PASSWORD}"

# Constructing the complete command
COMMAND="$JAVA_COMMAND $JAVA_OPTIONS $CLASSPATH $MAIN_CLASS $ADDITIONAL_ARGS"

# Executing the command in a new terminal
echo "Server is starting..."
$COMMAND &

