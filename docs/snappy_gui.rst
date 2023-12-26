SnappyHexMesh GUI Addon for Blender
===================================

.. image:: images/shmg_example_and_panel.png

Introduction
------------

This add-on turns `Blender <https://www.blender.org>`_
into a GUI for SnappyHexMesh, a volume mesh generation tool for
OpenFOAM®, the open source CFD (computational fluid dynamics) toolbox.
The add-on exports a complete OpenFOAM case folder structure, with
geometry and dictionary files, ready to run OpenFOAM commands
including *snappyHexMesh*. The aim of the add-on is to

* Ease the workflow for importing, updating, modifying and exporting
  3D surface meshes to OpenFOAM.
* Allow definition of most common SnappyHexMesh settings via Blender
  GUI, to reduce need for manual modification of OpenFOAM dictionary
  definitions.
* Require minimal Blender skills. Geometry can be modelled in any 3D
  modelling / CAD program which exports a surface mesh format that can
  be imported to Blender, such as STL or Wavefront OBJ.

The add-on generates OpenFOAM dictionary files for the surface mesh
objects in Blender. Dictionary creation is based on string
replacements using template files located in the
add-on's *skel* directory. The add-on is meant to work on
latest LTS release of `Blender`_ and latest stable
`OpenFOAM.com <https://www.openfoam.com/>`_ and
`OpenFOAM Foundation <https://openfoam.org/>`_
version of OpenFOAM.
Tested with Blender 3.6.

To learn to use SnappyHexMesh GUI, have a look at my video tutorial series
`Blender for OpenFOAM users <http://tkeskita.kapsi.fi/blender/>`_.


Current Status and Features
---------------------------

Currently implemented features include:

* Creation of basic OpenFOAM case structure, including export of
  dictionary files (most importantly snappyHexMeshDict) and meshes as
  STL files
* Optional creation of definition file for hexahedral base volume mesh with
  a defined cell size (blockMeshDict)
* Calculation of cell count for block volume mesh
* Definition of Surface Refinement Levels for surface meshes
* Creation of Feature Edges definition file (surfaceFeaturesDict)
* Definition of Surface Layers per surface
* Calculation of minimum and maximum bounds and surface area for each mesh.
  These information are also written to snappyHexMeshDict as comments.
* Creation of Face Zones and Cell Zones from surface meshes
* Specification of Refinement Regions (Volumes)

Installation and Start-up
-------------------------

* It is suggested to use newest LTS version of Blender,
  `download Blender LTS version here <https://www.blender.org/download/LTS/>`_.
* Add-on code is available at https://github.com/tkeskita/snappyhexmesh_gui
  --> Code --> Download zip.
* Start Blender, go to "Edit" --> "Preferences" --> "Add-ons" --> "Install"
  --> open the add-on zip file.
* Activate the "SnappyHexMesh GUI" add-on in Preferences.
  Add-on is located in Object category of Blender add-ons.
* Click "Save Preferences" to autoload add-on every time Blender is started

Add-on visibility
-----------------

Add-on is visible in Blender's 3D Viewport in Sidebar as a separate
tab in Object Mode. To view the add-on panels, you must

  * Select a mesh object (in 3D Viewport or in Outliner)
  * View Sidebar ("View" --> "Toggle Sidebar" or press "N" key in 3D Viewport)
  * Select "SnappyHexMesh GUI" tab in the Sidebar

Quickstart
----------

* Create surface meshes in any suitable 3D modelling tool and export
  in STL/OBJ format
* Import meshes to Blender ("File" --> "Import")
  or model geometry directly in Blender
* Adjust the add-on settings per object in Blender
* Save Blender file to an empty case folder
* Click **Export** button in the add-on to create OpenFOAM directories
  and files under the case folder

After export from Blender, you should be able to run following OpenFOAM
commands in the case folder in order:

* ``blockMesh``
* ``surfaceFeatureExtract`` (for openfoam.com version) or ``surfaceFeatures`` (for openfoam.org version of OpenFOAM)
* ``snappyHexMesh``
* ``checkMesh``
* Optionally run ``postProcess -time '1:'`` to generate cell center coordinate and cell volume fields

You can view the final mesh using `Paraview <https://www.paraview.org>`_.

Iterative Workflow
------------------

Here is an example iterative workflow for working the whole mesh
creation pipeline in a case folder. Meshing and reviewing the results
is fastest when you start with a fairly large block mesh *Cell
Length*, and tune only a few settings in the GUI at a time.

* Clean up case folder by running **Clean Case Dir**, or commands in terminal: ``rm -rf 1 2 3 constant system processor*``
* Make modifications in Blender, save file, and click the add-on **Export** button
* run OpenFOAM terminal commands: ``blockMesh; surfaceFeatureExtract; snappyHexMesh``
* Refresh Paraview to see updated mesh

Always check that the final mesh has correct scale, rotation and location.

Panels and Settings
-------------------

SnappyHexMesh GUI consists of three main Panels: SnappyHexMesh GUI
(top panel), Object Settings (middle panel) and Export Summary (bottom
panel). By default all panels are expanded.

.. image:: images/shmg_ui.png

SnappyHexMesh GUI Panel
^^^^^^^^^^^^^^^^^^^^^^^

This panel contains overall settings and tool buttons.
You can hover mouse cursor over fields to see tool tips for more
information.

* *Options* with CPU count and toggle icons:

  * *CPUs* specifies the number of cores for *decomposeParDict*
    (*scotch* decomposition method is the default for *decomposePar*)
  * *Do Castellation Phase*
  * *Do Snapping Phase*
  * *Do Layer Addition Phase*

* *Export Scale* is an optional scaling factor for STL geometry
  files and convertToMeters in blockMeshDict.
* *Fork* defines the fork of OpenFOAM for compatibility of generated files.
  Currently it only defines whether to produce *surfaceFeaturesDict*
  (for openfoam.org) or *surfaceFeatureExtractDict* (for
  openfoam.com).
* *Export path* defines path name where the add-on creates the OpenFOAM
  case files when the Export tool is run. The default value "//" means
  that the case folder is the same folder where Blender file is saved.
* *Generate Block Mesh* indicates that blockMeshDict is to be generated
  during export using *Cell Length* as a measure for cubical cell sides.
* *Cell Length* is the target length for the block mesh cube side,
  which will be created after export by running the OpenFOAM command
  *blockMesh*.
* *Max Non-Ortho* is the volume mesh quality measure for maximum
  non-orthogonality for SnappyHexMesh.

.. note::

  *Max Non-Ortho* is the most important mesh quality parameter. A small
  value produces mesh that is good for the numerical solution of flow
  equations. However, a small value restricts snapping and addition of
  surface layers. Meanwhile, a large value yields a mesh that snaps to
  surfaces better and allows better surface layer coverage, but the
  mesh may cause numerical issues for some solvers. The current
  default setup uses a small value (35) for the snapping phase, and a
  large value (75) for the *Relaxed Max Non-Ortho* option applied in
  the layer addition phase.

* *Min Twist* defines a minimum allowed value for twist of cell
  faces.

.. note::

  *Min Twist* is another important mesh quality parameter. A value
  close to one will produce flat faces, at the cost of worse snapping
  and decreased coverage of surface layers. A value close to zero allows twisted
  faces, which may cause numerical issues for solvers.
  However, snapping and layer addition are improved. The default
  configuration for *Min Twist* uses a medium value for snapping phase
  and a low value for layer addition phase.


The following Layer Addition Global Options are visible only if
*Do Layer Addition Phase* option is enabled.

.. warning::

   Addition of layers may create a mesh which causes numerical issues
   for some solvers.

* *Relaxed Max Non-Ortho* is the maximum non-orthogonality applied only
  for the Layer Addition phase.
* *Relaxed Min Twist* defines a minimum allowed value for twist of cell
  faces for the Layer Addition phase.
* *Feature Angle* defines the edge angle for feature detection. When
  angle is larger than this value, layers are collapsed (removed) at
  the edge. This affects layer building near corners. A large value
  creates layers which fill sharp corners, while a low value removes
  layers near corners.
* *Expansion Ratio* is the ratio of layer target thicknesses. Value larger than
  one will result in increasing layer thickness (from walls inwards).
* *Final Thickness* is the relative ratio of the final layer thickness
  to the base cell side length.
* *Min Thickness* is the minimum accepted relative layer thickness for
  any layer.

.. tip::

  Layer addition seems to work better with openfoam.com version of
  *snappyHexMesh* than with the openfoam.org version. For openfoam.org
  version, you can try to add layers incrementally, only two layers at
  a time. To do that, disable *Do Castellation Phase* and
  *Do Snapping Phase* options, modify the *Final Thickness* and
  *Min Thickness* parameters, *Export*, and then run *snappyHexMesh*
  again.

The panel buttons launch the following operators:

* **Clean Case Dir** command removes directory names *1-9, constant*,
  *system* and *processor\** if they exist in the *Export path*. This
  effectively cleans up the case folder from any lingering OpenFOAM
  files, so that after running *Export*, the case folder should
  contain only fresh files, ready for OpenFOAM.
* **Add Location In Mesh Object** will add an Empty object to Blender
  scene. The coordinates of this object is applied to specify the
  Location In Mesh for snappyHexMesh. If this object does not exist,
  zero coordinates are used for Location In Mesh.
* **Apply LocRotScale For All** resets the Object Transformation
  Properties (Location, Rotation and Scale) of all mesh objects to
  default values. This makes measurement values always unambiguous,
  regardless of whether you have the Local or Global Value option
  enabled. It is suggested to run this tool before mesh modifications
  to avoid possibility of accidentally inputting wrong values.
* **Export** tool creates and saves the OpenFOAM case files under
  *Export path* using the overall settings in this panel and Object
  Settings for each mesh object included in the export.
* If *ASCII STL* icon on right of *Export* tool is enabled, the STL
  files are written in ASCII text format instead of binary STL format.


Object Settings Panel
^^^^^^^^^^^^^^^^^^^^^

This panel shows settings for the active (selected) mesh object.
The panel top part shows information about the object. These
information are also added as comments in snappyHexMeshDict upon
export:
	   
* *Object* row shows the name of the active object.
* **Copy Settings to Objects** tool copies the SnappyHexMesh GUI
  settings from *the active object* (the last selected object) to all other *selected mesh
  objects*. This allows mass modification of SnappyHexMesh settings
  when dealing with numerous objects.
* *Object Bounds [min] [max]* shows the minimum and maximum
  coordinates of two box corners which span the volume included
  by the mesh object (bounding box).
* *Area* shows the summed surface area of all faces included in the
  object. **Warning:** Includes mesh errors, like overlapping faces, if
  there are any.

Rest of the panel includes object settings:

* *Include in Export* check box is used to mark which mesh objects are
  to be included in export.
* *Type* specifies the OpenFOAM patch type for this object.
* *Enable Snapping* check box marks inclusion/exclusion of this object
  for SnappyHexMesh snapping phase.
* *Surface Refinement Levels*, *Min* and *Max* specify the minimum and
  maximum level of cell refinements made next to the surfaces of this
  object.
* *Extract Feature Edges* check box marks whether Feature Edges (sharp
  edges) are to be extracted into eMesh format from this object (done
  by running the *surfaceFeatureExtract* or *surfaceFeatures* OpenFOAM
  utility).  If Feature Edges are extracted, then they are also
  assumed to be included for Feature Edge Snapping in SnappyHexMesh.
* *Feature Edge Level* defines a separate cell refinement level for
  Feature Edges.
* *Face Zone Type* decides the type of face zones that are to be
  created for surface:

  * **none**: No face zone or cell zone are to be created.
  * **internal**: Face zone is created with internal faces (each face
    is shared by two cells). The face zone is additionally added to
    *createBafflesDict*, just in case you want to run *createBaffles*
    later on to separate internal face zone into baffles.
  * **baffle**: Face zone is created as baffles (overlapping unshared
    boundary faces).
  * **boundary**: Face zone is created as boundaries (unshared boundary
    faces).

  **Note:** Face zone name is same as object name.

* *Cell Zone Type* defines the type of cell zones in relation to
  surface mesh, which is assumed to define a manifold surface which
  closes a volume:

  * none: No cell zone is to be created.
  * inside: Inside of the closed volume is to be included in cell zone.
  * outside: Outside of the closed volume is to be included in cell zone.

  **Note:** Cell zone name is same as object name.
  
  **Note 2:** Creation of a cell zone requires that face zone is also created
  for the same object.

* *Volume Refinement* specifies that some cells are to be refined accordingly:

  * none: No refinement.
  * inside: Cells inside of the closed volume are to be refined.
  * outside: Cells outside of the closed volume are to be refined.

* *Volume Refinement Level* shows the number of refinements for volume refinement.

  **Note:** For refinement volume objects, the typical settings
  are: *Type:* patch, *Enable Snapping:* disabled, *Extract Feature Edges:*
  disabled, and *Volume Refinement*: inside.

The following Layer Addition Settings are visible only if
*Do Layer Addition Phase* option is enabled.

* *Dict File Number* decides which *snappyHexMeshDict* file this
  Object will be added for layer addition. Value 1 means that layers
  for this Object surfaces will be specified in the default
  *snappyHexMeshDict* file. Values larger than one will create
  additional *snappyHexMeshDictX* files, where *X* is the *Dict File
  Number*. This allows additional layers to be added with consequent
  runs after the main **snappyHexMesh** run, by commands like
  **snappyHexMesh -dict system/snappyHexMeshDict2**. This is useful
  for creating intersecting layer patterns. In the cube example below,
  all three opposite cube face pairs have been separated, and layered in
  three separate *snappyHexMesh* runs.

  .. image:: images/shmg_intersecting_layers_on_a_cube.png

* *Surface Layers* specifies the number of surface layers that are to
  be added to surfaces of this Object. Addition of surface layers
  requires that the *Do Layer Addition Phase* option (icon at GUI top)
  is activated. Default value -1 means that no surface layers are
  specified. Value zero means that no layers are allowed.
* *Object Specific Layer Settings* allows optional definition of
  different layer addition settings for an object, instead of using
  the global options. The object specific settings are the same as the
  global settings described above: *Expansion Ratio*, *Final
  Thickness* and *Min Thickness*.


Export Summary Panel
^^^^^^^^^^^^^^^^^^^^

This panel summarizes the overall properties of export.

.. image:: images/shmg_panel_summary.png

* *Global Bounds [min] [max]* shows the minimum and maximum
  coordinates of the bounding box for all mesh objects included in the
  export.
* *Block Mesh Count* is an estimate for the number of cubic cells in
  Block Mesh which covers the Global Bounds using cube side length
  specified in *Cell Length* parameter. Block Mesh will be created by
  running OpenFOAM command *blockMesh*.
* *Objects included* lists all the mesh objects in Blender file, which
  will be exported when *Export* tool is run.
  
Example and tutorial links
--------------------------

A vessel example is located in the add-on's *example* folder called
*vessel.blend*, which showcases some of the features.

.. figure:: images/shmg_example_and_panel.png

   Vessel geometry, wall, zone and refinement volumes in surface mesh format viewed in `Blender`_

.. figure:: images/example_mesh_result.png

   Resulting volume mesh (snapped mesh without layers) from SnappyHexMesh viewed in `Paraview`_

- I made a tutorial video series `Blender for OpenFOAM users
  <http://tkeskita.kapsi.fi/blender/>`_ which has one tutorial for
  using SnappyHexMesh GUI

- A `Youtube tutorial illustrating the use of SnappyHexMesh GUI
  <https://www.youtube.com/watch?v=9XuDQOAPSL0>`_ (by
  `DaveyGravy <https://www.youtube.com/@daveygravy1207>`_,
  check also the other OpenFOAM related tutorial videos!).

Help and Feedback
-----------------

You are free to file bug reports, ask and give advice by using
`GitHub issues feature
<https://github.com/tkeskita/snappyhexmesh_gui/issues>`_.
Before asking, please try to see and run the vessel example (see
above) to make sure it works for you as expected. Also, please check
the FAQ section below.

Please provide a Blender file (no need to include anything else) with
a small example to illustrate your problem and describe the
issue. Please specify which OpenFOAM variant and version you use.

If you use this add-on, please star the project in GitHub!

FAQ
---

**Q: Why is my inlet/outlet/other patch cells malformed / big / not created?**

A: Your inlet/outlet/other patch does not coincide with (internal)
faces of the cells of the base block mesh. You may also need to apply
a sufficient level of refinement.

**Q: Why are some cell zones missing or wrong?**

A: Face normals are not consistent, or they are flipped. To fix face
normals, go to Edit Mode, select everything, and then run Mesh ->
Normals -> Recalculate Outside or Recalculate Inside, depending on
which side of the mesh surface is meant to be "inside" of the cell
zone.

For openfoam.com version, cell zone surfaces should enclose the whole
cell zone volume, while openfoam.org version needs only the surfaces
separating the cell zone from outside.

Tip: You can enable Face Orientation Overlay in Blender to visualize face
normal direction by color. Red color means that "inside direction" is
towards you, and blue color means that the "outside direction"
(the face normal direction) is towards you.

**Q: Why does a surface include faces in two different patches or face zones?**

A: Your case probably includes overlapping surfaces in two different
mesh objects. Remove the overlapping surfaces. See OpenFOAM tutorial
`heatTransfer/chtMultiRegionFoam/shellAndTubeHeatExchanger` for an example.

**Q: Why is there a world patch in the final mesh? / Why is my mesh leaking?**

A: You must always include a set of surfaces (in one or more mesh
objects) which define the outer boundaries of your
computational domain volume. Having a *world* patch in the final mesh
is an indication that your outer surface mesh is "leaking" (the final
mesh is extending outside the surfaces which should define the domain
volume). Leaking may also occur so that mesh extends inside surfaces
that define a volume object located inside the domain.
Leaking may be due to:

* Missing surfaces (holes in surface mesh).
* Big enough cracks (openings) exist in the edges between surfaces.
* *Enable Snapping* option is disabled for an object
* You may need to *Add Location In Mesh Object* to specify a point
  which is inside the mesh domain (otherwise it is assumed that origin
  is inside).
* Model is too far away from origin. Since Blender uses single
  precision floats and OpenFOAM uses double precision, it may help to
  move the model close to origin.

To find out the locations which are leaking, you must add a temporary
additional surface object (e.g. a cube or a plane) around model parts to
see where leaking stops.

**Q: Why is final mesh scale/rotation/placement wrong?**

A: Likely because Object Location/Rotation/Scale is wrong for some
object. If you need to do any movement/rotation/scaling when you
import your surface meshes into Blender to get the end result correct,
then it is good idea to use the *Apply LocRotScale for All*
operator/button to reset the scale before continuing. If you don't use
correct Object scale in Blender, then the measures shown in Blender are
incorrect. It is best to fix all location/rotation/scale issues in CAD
prior to exporting surface meshes to avoid this pitfall.

**Q: Cannot find file when extracting surface features**

If `surfaceFeatures` (for openfoam.org) or `surfaceFeatureExtract`
(for openfoam.com) command complains about cannot find file, make sure
that the Fork setting at GUI top is correct.

**Q: Layer addition crashes/segfaults on writeLayerSets**

A: If you get Segmentation fault (core dumped) with the following kind of
error message, it means that the layer addition failed to add any
layer cells. The crash seems to happen when snappy tries to write
layerSets with zero cells in the set::

  Added 0 out of 1234 cells (0%).
  Writing 0 added cells to cellSet addedCells
  [stack trace]
  =============
  #1  Foam::sigSegv::sigHandler(int) in /usr/lib/openfoam/openfoam2312/platforms/linux64GccDPInt32Opt/lib/libOpenFOAM.so
  #2  ? in /lib/x86_64-linux-gnu/libpthread.so.0
  #3  Foam::snappyLayerDriver::writeLayerSets(Foam::fvMesh const&, Foam::List<int> const&, Foam::Field<double> const&) const in /usr/lib/openfoam/openfoam2312/platforms/linux64GccDPInt32Opt/lib/libsnappyHexMesh.so
  #4  Foam::snappyLayerDriver::writeLayerData(Foam::fvMesh const&, Foam::List<int> const&, Foam::List<int> const&, Foam::Field<double> const&, Foam::Field<double> const&) const in /usr/lib/openfoam/openfoam2312/platforms/linux64GccDPInt32Opt/lib/libsnappyHexMesh.so
  ...

**Q: Help, my solver is crashing or diverging when I use a mesh from
snappyHexMesh!**

A: First, make sure that your solver setup is OK. To do this, use the
castellated mesh from snappyHexMesh case time directory 1 and try to
run the case with it. If it's not working, the issue might be in your
solver setup and not the mesh.

**Q: Help, my solver is crashing or diverging when I use a mesh from
snappyHexMesh, but it is not crashing when I use castellated mesh!**

A: Your mesh might be causing numerical issues for your solver. Since
you have one case which is failing and one case which is working, you
can try to change one thing at a time in your setup to home in on the
issue. Things you can try to change include:

- Disable layer addition (use the snapped-only mesh from time
  directory 2).
- If layers are required: Modify mesh criteria in the relaxed section
  of snappyHexMeshDict towards values listed in the
  meshQualityControls section. Or you can remove the relaxed section
  altogether. Warning: you layer coverage will decrease radically, as
  layer addition typically requires that snappyHexMesh is allowed to
  create low quality cells.
- Increase *Min Twist* and/or decrease *Max Non-Ortho* values to force
  snappyHexMesh to create high quality cells (at the cost of worse
  snapping and decreased layer coverage).

**Q: Help, my solver is still crashing, and I can't find the issue!**

A: You can try to post your case into a forum like
`CFD-Online <https://www.cfd-online.com/Forums/site-help-feedback-discussions/175429-guide-how-ask-question-forums.html#post612025>`_
but please read the instructions on the forum first!

**Q: Why build a SnappyHexMesh GUI on top of Blender?**

A: Mainly because of Blender's GUI Python API, 3D Viewport and surface
mesh modelling tools. Blender has powerful tools for polygon surface
modelling and modification, and is suitable also for precision
modelling required by engineering/scientific applications, although
the learning curve to take advantage of all features is steep.

**Q: How do I learn Blender?**

A: See links at https://openfoamwiki.net/index.php/Blender

**Q: How do I learn SnappyHexMesh and OpenFOAM?**

A: Details about SnappyHexMesh parameters can be found in annotated caseDicts:

  - For openfoam.com (development version), see
    https://develop.openfoam.com/Development/openfoam/-/blob/master/etc/caseDicts/annotated/snappyHexMeshDict
  - For openfoam.org (development version), see
    https://github.com/OpenFOAM/OpenFOAM-dev/blob/master/etc/caseDicts/annotated/snappyHexMeshDict
  - See also links in https://openfoamwiki.net/index.php/SnappyHexMesh

For OpenFOAM, see links at

  - https://holzmann-cfd.com/community/learn-openfoam,
  - https://openfoamwiki.net
  - https://www.cfd-online.com/Forums/openfoam/.

**Q: I'm actually looking for a GUI for OpenFOAM and not just a GUI for SnappyHexMesh..**

Please check `CfdOF for FreeCAD <https://github.com/jaheyns/cfdof>`_
and `Helyx-OS <https://engys.com/products/helyx-os>`_.
However, please be aware that OpenFOAM is developing at a rate which
no GUI developer can match, so the features supported by GUIs will
always be limited or potentially broken beyond supported OpenFOAM
versions.

OpenFOAM Trade Mark Notice
--------------------------

This offering is not approved or endorsed by OpenCFD Limited, producer
and distributor of the OpenFOAM software via www.openfoam.com, and
owner of the OPENFOAM® and OpenCFD® trade marks.
