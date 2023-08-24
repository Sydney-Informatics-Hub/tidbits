Title: Deploy R Shiny App on Remote Server
Date: 2020-04-07
Author: Sergio Pintaldi
Category: R
Tags: R, shiny, server, production, unitfile

# The Problem

Data Scientists are used to running R code with the click of a mouse using `Rstudio` and deploying it to a `Shiny Server` in the same way.

![]({attach}images/deploy_shiny_app/runapp_rstudio.png)

The reality is that many production servers use command line to run the process/webserver/app/... and use a master process (the supervisor) to control the execution of the app.

# A Simple Solution

All you need to run the app is to execute the following lines:

```bash
$ R -e "shiny::runApp()"
```

__Note__: the assumption here is that you are in a folder where an `app.R` is present (and where all your app code reside)!

Even better, you can improve your app by creating a `runapp.R` file, that look like this:

```r
library(optparse)

# declare script input options
args_list  <- list(
  make_option(
    c('-d', '--data-dir'), type = 'character', default = NULL,
    help = 'Data folder path', dest = 'data_dir'
  ),
  make_option(
    c('-u', '--username'), type = 'character', default = NULL,
    help = 'API username', dest = 'username'
  ),
  make_option(
    c('-p', '--password'), type = 'character', default = NULL,
    help = 'API password', dest = 'password'
  )
)

# parsing arguments
opt_parser <- OptionParser(option_list = args_list);
opt <- parse_args(opt_parser);

if (is.null(opt$username) | is.null(opt$password)) {
  print_help(opt_parser)
  stop('Must supply username and password', call. = FALSE)
}

username <- opt$username
password <- opt$password

shiny::runApp(host='127.0.0.1', port=7744, launch.browser=FALSE)
```

As you can see you can pass in the command line, arguments such as username and password, that can be used somewhere. Also you can add checks on those arguments. In the `runApp` command you can also specify the IP address and the port.


Until now nothing new... you can run this from a shell in your machine. Well in a server is not that different, you still need to run that command above, but the _"Supervisor"_ program will take care of that.

Usually Unix machines use the `systemd` as processes supervisor. It controls all the Linux OS processes, such as network and others. In order to let the `systemd` take care of your process (in this case the shiny app), you need to create a `unit` file (e.g. `myapp.service`), like this:

```bash
[Unit]
Description=My Shiny App
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/bin/R /path/to/my/app/runapp.R
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=MyShinyApp

[Install]
WantedBy=multi-user.target
```

And save in `/etc/systemd`. Then update the list of services `systemctl daemon-reload`, enable your service at startup `systemctl enable myapp.service`, and finally start your service `systemctl start myapp.service`.

Add a `syslog` config file to re-direct all logs of your process/App to a specific file. Create a new configuration file in `/etc/rsyslog.d/my_shiny_app.conf` with the following:

```bash
if $programname == 'MyShinyApp' then /path/to/log/file.log
& stop
```

Make sure permissions are all set for the specific logging file.

# Some More Background

People on the internet mention a few ways to deploy Shiny Apps on a server (see links in section below):

1. [Shiny (R)Server Open Source](https://rstudio.com/products/rstudio/#rstudio-server) - __FREE__
2. [Shiny Server Pro / R Studio Connect and Shinyapps.io](https://rstudio.com/products/shiny/shiny-server/) - __PAID!__
3. [ShinyProxy](https://www.shinyproxy.io/): open source enterprise level Shiny App server, with built-in functionality for LDAP authentication and no limits on concurrent usage.  - __FREE__
4. Custom architectures - __FREE/PAID__

![](https://appsilon.com/wp-content/uploads/2018/12/Scaling-Shiny-1-1-1024x714.png)

# My Conclusions/Gothas

* The approach above is equivalent to "Click-Upload-Run" your Shiny App on an open-source R Studio server. Both run a single R process!
* The approach above is more than enough to serve the app to a limited amount of users (< 50/100)
* Need to look into scaling up if the number of users is higher (ShinyProxy or R server pro/shinyconnect, etc.)

# Useful Links and More Reading

## Shiny Deployment

* HowTo put your Shiny App behind a proxy/load balancer: [https://support.rstudio.com/hc/en-us/articles/213733868-Running-Shiny-Server-with-a-Proxy](https://support.rstudio.com/hc/en-us/articles/213733868-Running-Shiny-Server-with-a-Proxy)
* [ShinyProxy](https://www.shinyproxy.io/)
* 4(5) ways to run Shiny App: [](https://appsilon.com/alternatives-to-scaling-shiny/)
* [Shiny in Production slides](https://speakerdeck.com/jcheng5/shiny-in-production?slide=47): talking about async, app profiling, etc.
* Create an App package with [Golem](https://thinkr-open.github.io/building-shiny-apps-workflow/stepbuild.html): good app cookie-cutter template generator
* [How to Build a Shiny App from scratch](https://bookdown.org/hadrien/how_to_build_a_shiny_app_from_scratch)
* [Shiny App profiling (R code profiling)](https://bookdown.org/hadrien/how_to_build_a_shiny_app_from_scratch/optimizing-your-application.html)
* [Shiny in Production workshop](https://kellobri.github.io/shiny-prod-book/)
* [Async Shiny App: Cranwhales](https://github.com/rstudio/cranwhales)


## Links on Unit Files:

* example [ProteHome](https://github.sydney.edu.au/informatics/pipe312-protehome-system/blob/master/protehome-prod.service)
* example [Digifarm](https://github.sydney.edu.au/informatics/PIPE-1185-DigiFarms-Deployment/blob/master/digifarm.service)
