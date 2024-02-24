import subprocess
import shlex

def execute_command(command):
    try:
        # Split the command into command and arguments for subprocess
        args = shlex.split(command)
        # Execute the command and capture the output
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Return the output and error (if any)
        return result.stdout, result.stderr
    except Exception as e:
        return '', str(e)

def redirect_io(command):
    # Detect I/O redirection in the command
    if '>' in command or '<' in command:
        # Handle I/O redirection and modify the command accordingly
        args = shlex.split(command)
        input_file = None
        output_file = None
        if '<' in args:
            input_index = args.index('<')
            input_file = args[input_index + 1]
            args = args[:input_index]
        if '>' in args:
            output_index = args.index('>')
            output_file = args[output_index + 1]
            args = args[:output_index]
        # Execute the command with I/O redirection
        input_handle = open(input_file, 'r') if input_file else subprocess.PIPE
        output_handle = open(output_file, 'w') if output_file else subprocess.PIPE

        # Handle subprocess.PIPE separately
        if isinstance(input_handle, int):
            input_handle = subprocess.PIPE
        if isinstance(output_handle, int):
            output_handle = subprocess.PIPE

        # Execute the command with I/O redirection
        result = subprocess.run(args, stdin=input_handle, stdout=output_handle, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    else:
        # Execute normally if there is no I/O redirection
        return execute_command(command)

def main():
    while True:
        # Prompt the user to enter a command
        command = input('7.shell> ')
        if command.lower() in ['exit', 'quit']:
            break
        output, error = redirect_io(command)
        if output:
            print(output)
        if error:
            print('Error:', error)

if __name__ == '__main__':
    main()
