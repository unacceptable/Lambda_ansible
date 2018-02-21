FROM amazonlinux

LABEL maintainer="robert@scriptmyjob.com"

RUN yum install python27-pip zip -y
RUN pip install virtualenv

COPY Ansible/ /Ansible/

RUN virtualenv -p /usr/bin/python2.7 /Ansible/

RUN cd /Ansible/ && \
    source bin/activate && \
    pip install ansible

RUN cd /Ansible/ && \
    zip /Ansible.zip \
        lambda.py \
        ansible.cfg \
        inventory/* \
        playbooks/*

RUN cd /Ansible/lib/python2.7/site-packages/ && \
        zip -r /Ansible.zip .; \
    cd -; \
    cd /Ansible/lib64/python2.7/site-packages/ && \
        zip -r /Ansible.zip .;
