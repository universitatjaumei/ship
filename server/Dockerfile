FROM phusion/baseimage
MAINTAINER Ricardo Borillo <borillo@gmail.com>

CMD ["/sbin/my_init"]

# System update

RUN apt-get update && apt-get install -y wget

# Configure SSH access with local keys

RUN rm -f /etc/service/sshd/down
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh && service ssh restart

ADD authorized_keys /tmp/authorized_keys
RUN cat /tmp/authorized_keys >> /root/.ssh/authorized_keys && rm -f /tmp/authorized_keys

# Install Java

RUN wget -q --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u45-b14/jdk-8u45-linux-x64.tar.gz -O /tmp/jdk.tar.gz && tar xvfz /tmp/jdk.tar.gz -C /usr/share

# Install Tomcat

RUN wget -q "http://apache.rediris.es/tomcat/tomcat-8/v8.0.26/bin/apache-tomcat-8.0.26.tar.gz" -O /tmp/tomcat.tar.gz \
   && tar xvfz /tmp/tomcat.tar.gz -C /usr/share/

RUN echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>" > /usr/share/apache-tomcat-8.0.26/conf/tomcat-users.xml \
   && echo "<tomcat-users>" >> /usr/share/apache-tomcat-8.0.26/conf/tomcat-users.xml \
   && echo "  <role rolename=\"manager-gui\"/>" >> /usr/share/apache-tomcat-8.0.26/conf/tomcat-users.xml \
   && echo "  <role rolename=\"manager-script\"/>" >> /usr/share/apache-tomcat-8.0.26/conf/tomcat-users.xml \
   && echo "  <user username=\"tomcat\" password=\"tomcat\" roles=\"manager-gui, manager-script\"/>" >> /usr/share/apache-tomcat-8.0.26/conf/tomcat-users.xml \
   && echo "</tomcat-users>" >> /usr/share/apache-tomcat-8.0.26/conf/tomcat-users.xml \
   && sed -i -e '2iexport JAVA_HOME=/usr/share/jdk1.8.0_45\' /usr/share/apache-tomcat-8.0.26/bin/catalina.sh \
   && sed -i -e '3iexport CATALINA_PID=/usr/share/apache-tomcat-8.0.26/tomcat.pid\' /usr/share/apache-tomcat-8.0.26/bin/catalina.sh

# Register Tomcat Service

RUN mkdir -p /etc/service/tomcat \
   && echo "#!/bin/bash" >> /etc/service/tomcat/run \
   && echo "/usr/share/apache-tomcat-8.0.26/bin/startup.sh" >> /etc/service/tomcat/run \
   && chmod +x /etc/service/tomcat/run

EXPOSE 22
EXPOSE 8080

# Final cleanup

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
