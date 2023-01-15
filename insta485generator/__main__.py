"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
import jinja2
import json
import shutil
import os

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('-o','--output', type=click.Path(), help='Output directory.') #exists might be false
@click.option('-v','--verbose', is_flag=True, default=False, help='Print more output.')

def main(input_dir, output, verbose):
    """Templated static website generator."""

    ########    Read in Config file #########
    input_dir = pathlib.Path(input_dir) # convert str to Path object
    if not input_dir.exists():
        print("Input directory doesn't exist")
        exit(1)
    
    ########    Read Config file    #########
    config_path = input_dir/"config.json" #convert str to Path object
    url = template  = context = ""
    with config_path.open() as f:
        config_info = json.load(f)
        for info in config_info:
            url = info["url"]
            template = info['template']
            context = info['context']

            #########   Format and Check Output Path #########
            url = url.lstrip("/")  # remove leading slash
            output_dir = input_dir/"html"  # default, can be changed with --output option
            if output: #if -o is specified, different output_dir specified
                output_dir = pathlib.Path(output) # convert str to Path object
            output_path = output_dir/url/"index.html"
            output_dir = output_dir/url
            if output_dir.exists():
                print("Output directory already exists")
                exit(1)
            
            #########   Render Templates #########
            template_dir = str(input_dir) + "/templates/" 
            from jinja2 import Environment, PackageLoader, select_autoescape
            template_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_dir),
                autoescape=jinja2.select_autoescape(['html', 'xml']),
            )

            template = template_env.get_template(template)

            output_dir.mkdir(parents=True) #check parents? for -output, already checked if dir exists
            output_path.touch(exist_ok=False) #create index.html file
            output_path.write_text(template.render(**context)) # recursive rendering of all dictionaries in 'context'
            if verbose:
                print("Rendered " + str(template) + " -> " + str(output_path))
    

    #########   Copy static_dir files into output_dir #########
    static_dir = input_dir/"static"
    if static_dir.exists():
        shutil.copytree(src=static_dir, dst=output_dir, dirs_exist_ok=True)
        if verbose:
            print("Copied " + str(input_dir) + " -> " + str(output_dir))



if __name__ == "__main__":
    main()
