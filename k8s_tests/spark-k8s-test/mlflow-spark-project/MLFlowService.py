import subprocess

class MLFlowService:
    def __init__(self, project_uri, experiment_name):
        self.project_uri = project_uri
        self.experiment_name = experiment_name

    def run(self, parameters=None):
        command = [
            "mlflow", "run",
            self.project_uri,
            "--experiment-name", self.experiment_name
        ]

        if parameters:
            for key, value in parameters.items():
                command.extend([f"--{key}", value])

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self._stream_logs(process)
            process.wait()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

        except subprocess.CalledProcessError as e:
            print(f"Error: Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _stream_logs(self, process):
        for line in process.stdout:
            print(line, end='')