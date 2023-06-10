<h1>POSRMORTEM</h1>
<hr/>
<b>Issue Summary:</b> Upon the release of ALX’s System Engineering & DevOps project 0x19 postmortem, on Jun 5, 2023 6:00 AM (WAT), we experienced an outage on Ubuntu 20.04.6 (Focal Fossa) container running an Apache web server. GET requests on the server led to Server Error’s with code 500 on the website.
<hr/>
<b>Timeline:</b>

<ol><li>The issue was encountered during 12:20pm</li>
<li>Our monitoring alert brought this issue to our awareness</li>
<li>Prompt action was taken to detect the root cause by running processes using ps aux. Two apache2 processes - root and www-data - were properly running.</li>
<li>Looked in the sites-available folder of the /etc/apache2/ directory. Determined that the web server was serving content located in /var/www/html/.</li>
<li>In one terminal, ran strace on the PID of the root Apache process. In another, curled the server. strace gave no useful information.</li>
<li>we ran strace on the PID of the root Apache process again, except on the PID of the www-data process. Thestrace revelead an -1 ENOENT (No such file or directory) error occurring upon an attempt to access the file /var/www/html/wp-includes/class-wp-locale.phpp.</li>
<li>Looked through files in the /var/www/html/ directory one-by-one, using Vim pattern matching to try and locate the erroneous .phpp file extension. Located it in the wp-settings.php file. (Line 137, require_once( ABSPATH . WPINC . '/class-wp-locale.php' );).</li>
<li>Removed the trailing p from the line.</li>
<li>Tested another curl on the server. 200 A-ok!</li>
<li>Wrote a Puppet manifest to automate fixing of the error.</li></ol>
<hr/>
<b>Root Cause:</b>

In full, the WordPress app was encountering a critical error in wp-settings.php when tyring to load the file class-wp-locale.phpp. The correct file name, located in the wp-content directory of the application folder, was class-wp-locale.php.

<ul><li>Patch involved a simple fix on the typo, removing the trailing p.</li></ul>
<hr/>
<b>Corrective and preventative measures:</b>

This outage was not a web server error, but an application error. To prevent such outages moving forward, please keep the following in mind.

<ul><li>Test the application before deploying. This error would have arisen and could have been addressed earlier had the app been tested.
Status monitoring. 
<li>Enable some uptime-monitoring service such as UptimeRobot to alert instantly upon outage of the website.</li></ul>
<em>A Puppet manifest 0-strace_is_your_friend.pp was written to automate fixing of any such identitical errors should they occur in the future. The manifest replaces any phpp extensions in the file /var/www/html/wp-settings.php with php.</em>
