title: Debugging bash 
author: Georgie Samaha
date: 2024-03-19
Category: unix
Tags: bash,debug,shell

## Bash essentials: debugging 

If you're new to the command-line interface (CLI), there's one thing you should know - unexpected errors or bugs is inevitable. Whether you're a seasoned user of the CLI or just dipping your toes in the world of the Unix shell, encountering typos, syntax errors, or unforeseen glitches is par for the course. 

Bash reigns supreme in the Unix shell, don't let [the snobs convince you it isn't worth learning](https://dev.to/jmfayard/bash-is-a-terrible-programming-language-but-whats-the-alternative--oc2) some basics if you're planning to work in the Unix shell and/or on an HPC. It is an approachable swiss army knife, especially in the context of research computing. 

Unfortunately, bash doesn't naturally handle errors very well. So, it is essential to include some error handling to ensure your scripts fail well when they encounter an error and you can easily tend to the source of those errors. Let's delve into some useful techniques: 

### Tough love

Let's force bash to behave in a way that eliminates the chances of some subtle bugs from the outset by starting our script with: 

```
#!/bin/bash
set -eou pipefail
```

You can use `set` to change the behaviour of the shell and control script execution. By incorporating this `set` directive above, you're doing the following: 

* `set -e` mandates immediate script termination upon any command failure 
* `set -u` treats references to undefined variables as errors which helps minimise the likelihood of subtle bugs caused by inadvertent variable omission 
* `set -o pipefail` ensures pipeline errors aren't masked. If any command in a pipeline fails, 

Run the scripts below as is, and then with `set` commands hashed out. Note the execution of the echo command after the failed commands with/without `set`. 

#### `set -e` 

This enables the errexit option which causes the shell to fail if a command returns a non-zero exit status. 

```
#!/bin/bash
set -e

# List the contents of a directory that doesn't exist
ls fake_directory

# This echo will not be printed as the ls command fails
echo "Execution finished!"
```

#### `set -u`

This is used to enable the nounset option which treats references to unset variables as errors. 

```
#!/bin/bash
set -u

# Try to access an undefined variable
echo "Value of undefined variable: $undefined_variable"

# This echo will not be printed after the undefined variable
echo "Execution finished!"
```

#### `set -o pipefail` 

This is used to enable the pipefail option, causing a pipeline to return a non-zero exit status if any component fails. 

```
#!/bin/bash
set -o pipefail

# Pipe the output of grep from a non-existant file to the sort command
grep "ABCDEFG" fake_file.txt | sort

# This will return a non-exit status of 2 
echo $?

# This echo will be printed after the non-zero exit status because we haven't run the errexit option
# Replace set -o pipefail with set -eo pipefail to stop echo command running
echo "Execution finished!"
```

### Beautiful echo 

Echo is a very simple solution for doublechecking the output of variables and the results of commands run within your scripts to confirm everything is as it should be: 

```
#!/bin/bash

echo "This is the start of the script" 

variable_A=hello
variable_B=world

echo variable_A is $variable_A
echo variable_B is $variable_B

echo doing something with $variable_A and $variable_B here

echo "This is the end of the script"
```

### The hero

Another nice set command we can use is to enable debugging mode with `set -x`. This will print each line of your script to the terminal as it is executed. It can be helpful in identifying where errors are occurring and if variables are correctly defined: 

```
#!/bin/bash
set -x

# Define some variables
foo="hello"
bar="world"

# Concatenate variables and print the result
result="$foo $bar"
echo "Result: $result"

# Do some maths
num1=10
num2=5
sum=$((num1 + num2))
echo "Sum: $sum"

# Access an undefined variable (intentional error)
echo "Undefined variable: $undefined_var"

# End debugging mode
set +x

# Additional commands that won't be debugged
echo "Script execution completed."
```

You can also run your script with `bash -x script.sh` without using `set -x` within the script. It does the same thing. 

### One step at a time 

If you're feeling particularly cautious, this [fancy `trap` command](https://wizardzines.com/comics/bash-debugging/) allows you to confirm every line of a script before it runs:  

```
trap '(read -p "[$BASH_SOURCE:$LINENO] $BASH_COMMAND")' DEBUG
```

Run it for our echo script above: 

```
#!/bin/bash
trap '(read -p "[$BASH_SOURCE:$LINENO] $BASH_COMMAND")' DEBUG

# Define some variables
foo="hello"
bar="world"

# Concatenate variables and print the result
result="$foo $bar"
echo "Result: $result"

# Do some maths
num1=10
num2=5
sum=$((num1 + num2))
echo "Sum: $sum"

# Additional commands that won't be debugged
echo "Script execution completed."
```

Hit enter to run each line. 

### The final word 

The `die()` function can be used to print an error message and terminate a script's execution. It takes one or more arguments and prints output to stderr:

```
#!/bin/bash

# Print error message if no inputs provided at execution
die() {
    local message=$1
    local error_file=$2

    # Print error message to stderr
    echo $message >&2

    # If an error file is specified, write the error message to the file
    if [ -n "$error_file" ]; then
        echo $message > $error_file
        echo Check error.log
    fi

    # Exit the script with a status code of 1
    exit 1
}

# Example usage of the die function
if [ $# -eq 0 ]; then
    die "Usage: $0 <filename> error.log"
    echo Check error.log
fi
```

### Resources 

* [Niko Heikkila's Don't use bash for scripting (all the time)](https://nikoheikkila.fi/blog/don-t-use-bash-for-scripting-all-the-time/)
* [Intermediate bash scripting](https://www.linode.com/docs/guides/an-intermediate-guide-to-bash-scripting/)
* [How to exit when errors occur in bash](https://www.geeksforgeeks.org/how-to-exit-when-errors-occur-in-bash-scripts/)
* [Best practices for scientific computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)
* [Some useful shell exit codes explained](https://github.com/SixArm/unix-shell-script-kit/blob/main/unix-shell-script-kit)
* [Julia Evans' Bite Size Bash! zine](https://wizardzines.com/zines/bite-size-bash/)
