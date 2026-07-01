# from __future__ import annotations
#%% import packages
from typing import Literal, Optional, Sequence, Union
from pathlib import Path


#%% 
def define_paths(
    markers: Union[str, Sequence[str]],
    root: Path | str,
    data_subdir: Path | str,
    results_dirname: str = "results",
    results_location: Literal["inside", "sibling"] = "sibling",
    create_results: bool = True,
) -> dict[str, Path]:
    """
    Define project root, data directory, and results directory.

    Parameters
    ----------
    root
        Project root path OR any path inside the project (we'll search upward
        for `markers` if `root` is not already the root).
    data_subdir
        Data directory path (relative to resolved root, or absolute).
        Example: "growth_data/Greenhouse_timecourse/raw_processed"
    results_dirname
        Name of the results directory to use/create.
    results_location
        "inside"  -> results_dir = data_dir / results_dirname
        "sibling" -> results_dir = data_dir.parent / results_dirname
    create_results
        If True, create results_dir (mkdir -p).
    markers
        Marker filenames that identify the project root.

    Returns
    -------
    dict with keys: root, data_dir, results_dir
    """ 

    #write function to define paths for data and results directories, to be used in all scripts
    def _find_project_root(
        start:Path | str,
        markers: Union[str, Sequence[str]]
        ) -> Path:

        start = Path(start).resolve() 
        if start.is_file():
            start = start.parent
        
        # Require markers explicitly
        # ensure string is not converted to a tuple of charcaters
        if isinstance(markers, str):
            markers = (markers,)
        # else statement for if use passes more than one marker string
        else:
            markers = tuple(markers)

        if not markers:
            raise ValueError(
                "You must provide at least one marker filename"
            )

        for p in (start, *start.parents):
            if any((p / m).exists() for m in markers):
                return p

        raise FileNotFoundError(f"Could not find project root (missing {markers}) from {start}")
        
    root = Path(root).resolve() 
    resolved_root = _find_project_root(root,markers)

    data_dir = Path(data_subdir)
    if not data_dir.is_absolute():
        data_dir = (resolved_root / data_dir).resolve()
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")
    if not data_dir.is_dir():
        raise NotADirectoryError(f"Data path is not a directory: {data_dir}")

    if results_location == "inside":
        results_dir = data_dir / results_dirname
    elif results_location == "sibling":
        results_dir = data_dir.parent / results_dirname
    else:
        raise ValueError("results_location must be 'inside' or 'sibling'")

    if create_results:
        results_dir.mkdir(parents=True, exist_ok=True)

    return {"root": resolved_root, "data_dir": data_dir, "results_dir": results_dir}
# %%
