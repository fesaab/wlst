from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ServiceConfigurationMBean

def disableMessageTracing(configMB, service):
	'''
	Check if the message tracing is enabled and if so, disable it.
	'''
	if configMB.isMessageTracingEnabled(service) == 1:
		print "Message Tracing Disabled: ", service
		configMB.setMessageTracingEnabled(service, False)


# connect to OSB domain
username = 'username'
password = 'password'
url = 't3://host:port'
connect(username, password, url)

# prepare to do changes on the domain
domainRuntime()

# create a session to disable the logs
sessionMB = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
sessionName = "Auto_Disable_Logs_" + str(System.currentTimeMillis())
sessionMB.createSession(sessionName)
print "Created session", sessionName

# Recover the ServiceConfigurationMBean for this session
namePattern = "com.bea:Name=" + str(ServiceConfigurationMBean.NAME) + "." + str(sessionName) + ",Type=" + str(ServiceConfigurationMBean.TYPE)
objName = mbs.queryNames(ObjectName(namePattern), None)[0]
configMB = JMX.newMBeanProxy(mbs, objName, Class.forName(ServiceConfigurationMBean.TYPE))
print "Projects configuration recovered", configMB

# Disable the Message Tracing of all the Proxies
for proxy in configMB.getProxyRefs():
	disableMessageTracing(configMB, proxy)

# Disable the Message Tracing of all the Businesses
for business in configMB.getBusinessServiceRefs():
	disableMessageTracing(configMB, business)

# Activate the session and exit
sessionMB.activateSession(sessionName, "Disabled message tracing")
print "Successfully activated session", sessionName
exit()