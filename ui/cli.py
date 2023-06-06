from rich.console import Console

banner = r"""
                       [green3]=*%@@%#=[/green3]       
    		     [green3]:@@#-::-*@@:[/green3]     
 ____               [green3]:@@.       @@:[/green3] _               _    
|  _ \ __ _ ___ ___ [green3]:@@+#@@@@%+@@:[/green3]| |    ___   ___| | __
| |_) / _` / __/ __|[green3]@@@@@/  \@@@@@[/green3]| |   / _ \ / __| |/ /     
|  __/ (_| \__ \__ [green3]#@@@@@\__/@@@@@#[/green3] |__| (_) | (__|   <      
|_|   \__,_|___/___[green3]:@@@@@@:.@@@@@@:[/green3]_____\___/ \___|_|\_\       
                    [green3]:%@@@@@@@@@@%:[/green3]  
		      [green3]:+#@@@@#+:[/green3]     			 """


class Cli():
    def __init__(self) -> None:
        self.console = Console()
        self.prefix = '[purple3]PASS🔒LOCK[/purple3]$'

    def run(self):
        self.console.print(banner, style='bold purple3')

    def add(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def find(self):
        pass
