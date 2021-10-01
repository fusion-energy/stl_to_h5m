from pymoab import core, types
from pathlib import Path
from typing import Tuple, List
import numpy as np


def stl_to_h5m(
    files_with_tags: List[Tuple[str, str]],
    h5m_filename: str = "dagmc.h5m",
) -> str:
    """Converts stl files into DAGMC compatible h5m file using PyMOAB. The
    DAGMC file produced has not been imprinted and merged unlike the other
    supported method which uses Cubit to produce an imprinted and merged
    DAGMC geometry. This could result in overlaping geometry and lost particles
    during transport. Ensure your STL files don't overlap when using this
    convertion method. Consider using cad-to-h5m if imprinting and merging is
    required.

    Arguments:
        files_with_tags: The filenames of the input STL files with associated
            materials tags in the form of a list of tuples. For example
            [("file1.stl", "material_tag_1"), ("file2.stl", "material_tag_2")].
        h5m_filename: the file name of the output h5m file which is suitable for
            use in DAGMC enabled particle transport codes.

    Returns:
        The filename of the DAGMC file created
    """

    path_filename = Path(h5m_filename)

    if path_filename.suffix != ".h5m":
        raise ValueError('The h5m filename must end with ".h5m"')

    path_filename.parents[0].mkdir(parents=True, exist_ok=True)

    moab_core, moab_tags = _define_moab_core_and_tags()

    surface_id = 1
    volume_id = 1

    for entry in files_with_tags:
        stl_filename = entry[0]
        material_tag = entry[1]

        moab_core = _add_stl_to_moab_core(
            moab_core,
            surface_id,
            volume_id,
            material_tag,
            moab_tags,
            stl_filename)
        volume_id += 1
        surface_id += 1

    all_sets = moab_core.get_entities_by_handle(0)

    file_set = moab_core.create_meshset()

    moab_core.add_entities(file_set, all_sets)

    moab_core.write_file(str(path_filename))

    return str(path_filename)


def _define_moab_core_and_tags() -> Tuple[core.Core, dict]:
    """Creates a MOAB Core instance which can be built up by adding sets of
    triangles to the instance

    Returns:
        (pymoab Core): A pymoab.core.Core() instance
        (pymoab tag_handle): A pymoab.core.tag_get_handle() instance
    """

    # create pymoab instance
    moab_core = core.Core()

    tags = dict()

    sense_tag_name = "GEOM_SENSE_2"
    sense_tag_size = 2
    tags["surf_sense"] = moab_core.tag_get_handle(
        sense_tag_name,
        sense_tag_size,
        types.MB_TYPE_HANDLE,
        types.MB_TAG_SPARSE,
        create_if_missing=True,
    )

    tags["category"] = moab_core.tag_get_handle(
        types.CATEGORY_TAG_NAME,
        types.CATEGORY_TAG_SIZE,
        types.MB_TYPE_OPAQUE,
        types.MB_TAG_SPARSE,
        create_if_missing=True,
    )

    tags["name"] = moab_core.tag_get_handle(
        types.NAME_TAG_NAME,
        types.NAME_TAG_SIZE,
        types.MB_TYPE_OPAQUE,
        types.MB_TAG_SPARSE,
        create_if_missing=True,
    )

    tags["geom_dimension"] = moab_core.tag_get_handle(
        types.GEOM_DIMENSION_TAG_NAME,
        1,
        types.MB_TYPE_INTEGER,
        types.MB_TAG_DENSE,
        create_if_missing=True,
    )

    # Global ID is a default tag, just need the name to retrieve
    tags["global_id"] = moab_core.tag_get_handle(types.GLOBAL_ID_TAG_NAME)

    return moab_core, tags


def _add_stl_to_moab_core(
    moab_core: core.Core,
    surface_id: int,
    volume_id: int,
    material_name: str,
    tags: dict,
    stl_filename: str,
) -> core.Core:
    """Computes the m and c coefficients of the equation (y=mx+c) for
    a straight line from two points.

    Args:
        moab_core: A moab core object
        surface_id: the id number to apply to the surface
        volume_id: the id numbers to apply to the volumes
        material_name: the material tag name to add. the value provided will
            be prepended with "mat:" unless it is "reflective" which is
            a special case and therefore will remain as is.
        tags: A dictionary of the MOAB tags
        stl_filename: the filename of the stl file to load into the moab core

    Returns:
        An updated pymoab.core.Core() instance
    """

    surface_set = moab_core.create_meshset()
    volume_set = moab_core.create_meshset()

    # recent versions of MOAB handle this automatically
    # but best to go ahead and do it manually
    moab_core.tag_set_data(tags["global_id"], volume_set, volume_id)

    moab_core.tag_set_data(tags["global_id"], surface_set, surface_id)

    # set geom IDs
    moab_core.tag_set_data(tags["geom_dimension"], volume_set, 3)
    moab_core.tag_set_data(tags["geom_dimension"], surface_set, 2)

    # set category tag values
    moab_core.tag_set_data(tags["category"], volume_set, "Volume")
    moab_core.tag_set_data(tags["category"], surface_set, "Surface")

    # establish parent-child relationship
    moab_core.add_parent_child(volume_set, surface_set)

    # set surface sense
    sense_data = [volume_set, np.uint64(0)]
    moab_core.tag_set_data(tags["surf_sense"], surface_set, sense_data)

    # load the stl triangles/vertices into the surface set
    moab_core.load_file(stl_filename, surface_set)

    group_set = moab_core.create_meshset()
    moab_core.tag_set_data(tags["category"], group_set, "Group")

    # reflective is a special case that should not have mat: in front
    if not material_name == "reflective":
        dag_material_tag = "mat:{}".format(material_name)
    else:
        dag_material_tag = material_name

    moab_core.tag_set_data(tags["name"], group_set, dag_material_tag)
    moab_core.tag_set_data(tags["geom_dimension"], group_set, 4)

    # add the volume to this group set
    moab_core.add_entity(group_set, volume_set)

    return moab_core
