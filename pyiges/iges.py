from tqdm import tqdm

from pyiges import geometry
from pyiges.check_imports import assert_full_module_variant, pyvista, vtkAppendPolyData
from pyiges.entity import Entity

class Iges:
    """pyiges.Iges object

    Parameters
    ----------
    filename : str
        Filename of an IGES file.

    Examples
    --------
    >>> import pyiges
    >>> from pyiges import examples
    >>> iges = pyiges.read(examples.impeller)
        pyiges.Iges object
        Description:
        Number of Entities: 4615
    """

    def __init__(self, filename):
        self._read(filename)
        self._desc = ""

    def entities(self):
        """Return a list of all entities

        Examples
        --------
        >>> iges.entities
        [<pyiges.geometry.Point at 0x7f7056069c10>,
         <pyiges.geometry.Point at 0x7f7056069790>,
         <pyiges.geometry.Point at 0x7f7056069a50>,
         <pyiges.geometry.Point at 0x7f7056069b10>,
         <pyiges.entity.Entity at 0x7f7056069910>]
        """

    @assert_full_module_variant
    def to_vtk(
        self,
        lines=True,
        bsplines=True,
        surfaces=True,
        points=True,
        delta=0.025,
        merge=True,
        progress=tqdm,
    ):
        """Converts entities to a vtk object

        Parameters
        ----------
        lines : bool, optional
            Convert lines.

        surfaces : bool, optional
            Convert B-Spline surfaces.

        points : bool, optional
            Convert points.

        delta : float, optional
            Resolution when converting spline entities.  Higher
            resolution creates a better plot at the cost of computing
            time.

        merge : bool, optional
            Merge all converted entities into one output.

        progress: function, optional
            Report conversion progress by use of this function. Example::

                def silent_progress(iterable, *args, **kwargs):
                    return iterable

            Passing progress=silent_progress will show no progress, the
            default is to use tqdm for progress reporting.

        Returns
        -------
        surf : pyvista.PolyData or pyvista.MultiBlock
            Geometry represented as ``pyvista.PolyData`` if merged or
            a ``MultiBlock`` if unmerged.

        Examples
        --------
        Convert all entities except for surfaces to vtk

        >>> lines = iges.to_vtk(surfaces=False)
        >>> print(lines)
        PolyData (0x7f700c79f3d0)
          N Cells:	2440
          N Points:	96218
          X Bounds:	-4.299e+01, 6.912e+14
          Y Bounds:	-4.255e+01, 6.290e+14
          Z Bounds:	-9.980e+02, 6.702e+14
          N Arrays:	0
        """
        items = pyvista.MultiBlock()
        for entity in progress(self, desc="Converting entities to vtk"):
            if isinstance(entity, geometry.RationalBSplineCurve) and bsplines:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, geometry.RationalBSplineSurface) and surfaces:
                items.append(entity.to_vtk(delta))
            elif isinstance(entity, geometry.Line) and lines:
                items.append(entity.to_vtk())
            elif isinstance(entity, geometry.Point) and points:
                items.append(entity.to_vtk())

        # merge to a single mesh
        if merge:
            afilter = vtkAppendPolyData()
            for item in items:
                afilter.AddInputData(item)
            afilter.Update()

            return pyvista.wrap(afilter.GetOutput())

        return items

    def points(self, as_vtk=False, merge=False, **kwargs):
        """Return all points"""
        return self._return_type(geometry.Point, as_vtk, merge, **kwargs)

    def edge_lists(self, as_vtk=False, merge=False, **kwargs):
        """All Edge Lists"""
        return self._return_type(geometry.EdgeList, as_vtk, merge, **kwargs)

    def vertex_lists(self, as_vtk=False, merge=False, **kwargs):
        """All Point Lists"""
        return self._return_type(geometry.VertexList, as_vtk, merge, **kwargs)

    def lines(self, as_vtk=False, merge=False, **kwargs):
        """All lines"""
        return self._return_type(geometry.Line, as_vtk, merge, **kwargs)

    def bsplines(self, as_vtk=False, merge=False, **kwargs):
        """All bsplines"""
        return self._return_type(geometry.RationalBSplineCurve, as_vtk, merge, **kwargs)

    def bspline_surfaces(self, as_vtk=False, merge=False, **kwargs):
        """All bsplines

        Examples
        --------
        Convert and plot all bspline surfaces.  This takes a while
        since the geometry tessellation is done in pure python by
        ``geomdl``.  Reduce the conversion time by setting delta to a
        larger than default value (0.025)

        >>> mesh = iges.bspline_surfaces(as_vtk=True, merge=True)
        >>> mesh.plot()

        Alternatively, just extract the B-REP surfaces and extract
        their parameters

        >>> bsurf = iges.bspline_surfaces()
        >>> bsurf[0]
        Rational B-Spline Surface
            Upper index of first sum:        3
            Upper index of second sum:       3
            Degree of first basis functions: 3
            Degree of second basis functions: 3
            Open in the first direction
            Open in the second direction
            Polynomial
            Periodic in the first direction
            Periodic in the second direction
            Knot 1: [0. 0. 0. 0. 1. 1. 1. 1.]
            Knot 2: [0. 0. 0. 0. 1. 1. 1. 1.]
            u0: 1.000000
            u1: 0.000000
            v0: 1.000000
            v1: 128.000000
            Control Points: 16
        """
        return self._return_type(
            geometry.RationalBSplineSurface, as_vtk, merge, **kwargs
        )

    def circular_arcs(self, to_vtk=False, merge=False, **kwargs):
        """All circular_arcs"""
        return self._return_type(geometry.CircularArc, to_vtk, merge, **kwargs)

    def conic_arcs(self, as_vtk=False, merge=False, **kwargs):
        return self._return_type(geometry.ConicArc, as_vtk, merge, **kwargs)

    def faces(self, as_vtk=False, merge=False, **kwargs):
        return self._return_type(geometry.Face, as_vtk, merge, **kwargs)

    def loops(self, as_vtk=False, merge=False, **kwargs):
        return self._return_type(geometry.Loop, as_vtk, merge, **kwargs)

    def _return_type(self, iges_type, to_vtk=False, merge=False, **kwargs):
        """Return an iges type"""
        items = []
        for entity in self:
            if isinstance(entity, iges_type):
                if to_vtk:
                    items.append(entity.to_vtk(**kwargs))
                else:
                    items.append(entity)

        # merge to a single mesh
        if merge and to_vtk:
            afilter = vtkAppendPolyData()
            for item in items:
                afilter.AddInputData(item)
            afilter.Update()

            return pyvista.wrap(afilter.GetOutput())

        return items

    def __iter__(self):
        yield from self._entities

    def __len__(self):
        return len(self._entities)

    def __repr__(self):
        info = "pyiges.Iges object\n"
        info += "Description: %s\n" % self._desc
        info += "Number of Entities: %d" % len(self)
        return info

    def from_pointer(self, ptr):
        """Return an iges object according to an iges pointer"""
        return self[self._pointers[ptr]]

    def _parse_separators_from_first_global_line(self, line):
        print(line)
        if line[0] == ",":
            a = ","
            if line[1] == a:
                b = ";"
            elif line[1:3] == "1H":
                b = line[3]
            else:
                raise RuntimeError("Invalid Global section format")
        elif line[0:2] == "1H":
            a = line[2]
            if line[4:6] == "1H":
                b = line[6]
            elif line[3] == a:
                b = ";"
            else:
                raise RuntimeError("Invalid Global section format")
        else:
            raise RuntimeError("Invalid Global section format")
        
        self.record_sep = b
        self.param_sep = a

    def _read(self, filename):

        entity_dict = {
            # Curve and surface entities.  See IGES spec v5.3, p. 38, Table 3
            100: geometry.CircularArc,  # Circular arc
            102: Entity,                # Composite curve
            104: geometry.ConicArc,     # Conic arc
            108: Entity,                # Plane
            110: geometry.Line,         # Line
            112: Entity,                # Parametric spline curve
            114: Entity,                # Parametric spline surface
            116: geometry.Point,        # Point
            118: Entity,                # Ruled surface
            120: Entity,                # Surface of revolution
            122: Entity,                # Tabulated cylinder
            124: geometry.Transformation,           # Transformation matrix
            126: geometry.RationalBSplineCurve,     # Rational B-spline curve
            128: geometry.RationalBSplineSurface,   # Rational B-spline surface
            
            # CSG Entities. See IGES spec v5.3, p. 42, Section 3.3
            150: Entity,                # Block

            # B-Rep entities.  See IGES spec v5.3, p. 43, Section 3.4
            186: Entity,                # B-Rep entity

            # Annotation entities.  See IGES spec v5.3, p. 46, Section 3.5
            202: Entity,                # Annotation entity

            # Structural entities.  See IGES spec v5.3, p. 50, Section 3.6
            132: Entity,                # Structural entity

            # Geometry entities.  See IGES spec v5.3, p. 52, Section 3.7
            502: geometry.VertexList,   # Vertex list
            504: geometry.EdgeList,     # Edge list
            508: geometry.Loop,         # Loop
            510: geometry.Face,         # Face
        }

        def _create_entity(head_reader, lines):
            """_summary_

            Args:
                line (_type_): _description_
                first_dict_line (_type_): _description_
            """
            data = lines[head_reader]
            first_row = lines[head_reader]
            second_row = lines[head_reader + 1]

            entity_type_number = int(data[0:8].strip())
            e = entity_dict.get(entity_type_number, Entity)(self)

            data = first_row
            e.add_section(data[0:8], "entity_type_number")
            e.add_section(data[8:16], "parameter_pointer")
            e.add_section(data[16:24], "structure")
            e.add_section(data[24:32], "line_font_pattern")
            e.add_section(data[32:40], "level")
            e.add_section(data[40:48], "view")
            e.add_section(data[48:56], "transform")
            e.add_section(data[56:65], "label_assoc")
            e.add_section(data[65:72], "status_number")
            e.sequence_number = int(data[73:].strip())

            data = second_row
            e.add_section(data[8:16], "line_weight_number")
            e.add_section(data[16:24], "color_number")
            e.add_section(data[24:32], "param_line_count")
            e.add_section(data[32:40], "form_number")
            e.add_section(data[56:64], "entity_label", type="string")
            e.add_section(data[64:72], "entity_subs_num")
            return e

        def _read_parameters(head_reader, lines):
            string = ""
            entity_pointers = []
            n_processed_lines = 0

            while True:
                string += lines[head_reader+n_processed_lines][:64]
                entity_pointers.append(int(lines[head_reader][64:72].strip()))
                n_processed_lines += 1

                if string.strip()[-1] == self.record_sep:
                    break

            # assert all([e in set(entity_pointers) for e in entity_pointers]) # Check that all pointers are indicating the same entity
            # print(entity_pointers)
            # print(pointer_dict)
            parameters = string.strip()[:-1].split(self.param_sep)
            entity_list[pointer_dict[entity_pointers[0]]]._add_parameters(parameters)
            return n_processed_lines


        with open(filename) as f:
            lines = f.readlines()

        entity_list = []
        entity_index = 0
        self.global_string = []
        pointer_dict = {}
        entities_to_discard = []

        idx = 0
        self._parse_separators_from_first_global_line(lines[1])

        while idx < len(lines):
            line = lines[idx]
            data = line[:80]
            id_code = line[72]

            if id_code == "S":  # Start
                desc = line[:72].strip()
                idx += 1

            elif id_code == "G":  # Global
                self.global_string += [''.join(data)]  # Consolidate all global lines
                idx += 1

            elif id_code == "D":  # Directory entry
                entity = _create_entity(idx, lines)
                entity_list.append(entity)
                pointer_dict.update({entity.sequence_number: entity_index})

                entity_index += 1
                idx += 2 # Skip the next line, which is the continuation of the directory entry
                    
            elif id_code == "P":  # Parameter data

                skip_lines = _read_parameters(idx, lines)
                idx += skip_lines

            elif id_code == "T":  # Terminate
                self.last_line = line
                break

        print(pointer_dict)
        # for e in entities_to_discard:
        #     try:
        #         entity_list.remove(e)
        #     except:
        #         pass

        self._entities = entity_list
        self.desc = desc
        self._pointers = pointer_dict

    def write(self, filename):
        
        line_length = 80
        
        # Filter entities to remove artifacts and build ID Map to fix flipping.
        #kept_types = {112, 114, 118, 120, 122, 124, 126, 128, 142, 144, 186, 502, 504, 508, 510}
        kept_types = {124, 128}
        
        filtered_entities = []
        id_map = {} # Maps old_sequence -> new_sequence
        current_seq = 1
        for e in self._entities:
            etype = e.d.get("entity_type_number")
            if etype in kept_types:
                filtered_entities.append(e)
                if hasattr(e, 'sequence_number') and e.sequence_number is not None:
                    id_map[e.sequence_number] = current_seq
                current_seq += 2        
        
        # Initialize counters
        self.directory_counter = 0
        self.global_counter = 0
        self.parameter_counter = 0        
        
        # Storage for calculated line counts (fixes explosion)
        self.calculated_param_start = []
        self.calculated_line_count = []

        def start_line():
            start_line = list(self.desc)
            start_line.extend([" "] * (line_length - len(start_line)))  
            start_line[72] = "S"
            start_line[73:line_length-1] = str(1).rjust(7)
            start_line[-1] = "\n"
            return "".join(start_line)
     
        # NEW Remap pointers and write correct line counts
        def directory_lines():
            dir_string = ""
            for i, e in enumerate(filtered_entities, start=1):
                
                # Helper to remap pointers using id_map
                def get_remapped_ptr(key):
                    old_ptr = e.d.get(key)
                    if old_ptr is None or old_ptr == 0: return 0
                    return id_map.get(old_ptr, 0)

                # Retrieve calculated location data
                param_start = self.calculated_param_start[i-1]
                line_count = self.calculated_line_count[i-1]

                # LINE 1
                line = [" "] * line_length
                line[0:8] = str(e.d.get("entity_type_number", 0)).rjust(8)
                line[8:16] = str(param_start).rjust(8) # Correct Start Index
                line[16:24] = str(get_remapped_ptr("structure")).rjust(8)
                line[24:32] = str(get_remapped_ptr("line_font_pattern")).rjust(8)
                line[32:40] = str(get_remapped_ptr("level")).rjust(8)
                line[40:48] = str(get_remapped_ptr("view")).rjust(8)
                line[48:56] = str(get_remapped_ptr("transform")).rjust(8) # FIXES FLIPPING
                line[56:64] = str(get_remapped_ptr("label_assoc")).rjust(8)
                line[64:72] = '{:08d}'.format(e.d.get("status_number", 0)).rjust(8)
                line[72] = "D"
                line[73:line_length-1] = str(i*2-1).rjust(7)
                line[-1] = "\n"
                first_line = "".join(line)

                # LINE 2
                line = [" "] * line_length
                line[0:8] = str(e.d.get("entity_type_number", 0)).rjust(8)
                line[8:16] = str(e.d.get("line_weight_number", 0)).rjust(8)
                line[16:24] = str(get_remapped_ptr("color_number")).rjust(8)
                line[24:32] = str(line_count).rjust(8) # Correct Line Count
                line[32:40] = str(e.d.get("form_number", 0)).rjust(8)
                line[40:48] = str(0).rjust(8) 
                line[48:56] = str(0).rjust(8) 
                line[56:64] = str(e.d.get("entity_label", "") or "").rjust(8)
                line[64:72] = str(e.d.get("entity_subs_num", 0)).rjust(8)
                line[72] = "D"
                line[73:line_length-1] = str(i*2).rjust(7)
                line[-1] = "\n"
                second_line = "".join(line)
                
                dir_string += first_line
                dir_string += second_line
                self.directory_counter += 2
            return dir_string

        # NEW chunker
        def chunker(full_string):
            tokens = full_string.replace('\n', '').strip().split(',')
            lines = []
            current_line = ""
            
            for i, token in enumerate(tokens):
                separator = "," if i < len(tokens) - 1 else ""
                chunk = token + separator
                
                # Hard break only if token > 64 chars (rare)
                if len(chunk) > 64:
                    if current_line: 
                        lines.append(current_line)
                        current_line = ""
                    for k in range(0, len(chunk), 64):
                        lines.append(chunk[k:k+64])
                    continue

                if len(current_line) + len(chunk) <= 64:
                    current_line += chunk
                else:
                    lines.append(current_line)
                    current_line = chunk
            
            if current_line:
                lines.append(current_line)
            return lines
        
        # def parameter_lines():
        #     param_string = ""
        #     sequence = 0
        #     self.parameter_ref = {}

        #     for i, e in enumerate(self._entities, start=1):

        #         no_lines = 0
        #         current_string = e.parameter_string
        #         if isinstance(current_string, tuple): ################# splines
        #             # print(current_string)

        #             first_string = current_string[0]
        #             if len(first_string) > 64:
        #                 wrapped_params = my_wrapper(first_string)
        #             else:
        #                 wrapped_params = [first_string]
        #             new_lines = ""
        #             for p in wrapped_params:
        #                 new_ = [" "] * line_length
        #                 new_[0:64] = p.ljust(64)
        #                 new_[65:72] = '{:07d}'.format(reverse_pointers[i-1]).rjust(7)
        #                 sequence += 1
        #                 new_[72] = "P"
        #                 new_[73:line_length-1] = str(sequence).rjust(7)
        #                 new_[-1] = "\n"
        #                 new_lines += "".join(new_)
        #                 self.parameter_counter += 1
        #                 no_lines += 1

        #             for p in current_string[1].split('\n'):
        #                 new_ = [" "] * line_length
        #                 new_[0:64] = p.ljust(64)
        #                 new_[65:72] = '{:07d}'.format(reverse_pointers[i-1]).rjust(7)
        #                 sequence += 1
        #                 new_[72] = "P"
        #                 new_[73:line_length-1] = str(sequence).rjust(7)
        #                 new_[-1] = "\n"
        #                 new_lines += "".join(new_)
        #                 self.parameter_counter += 1
        #                 no_lines += 1

        #             first_string = current_string[2]
        #             if len(first_string) > 64:
        #                 wrapped_params = my_wrapper(first_string)
        #             else:
        #                 wrapped_params = [first_string]
        #             for p in wrapped_params:
        #                 new_ = [" "] * line_length
        #                 new_[0:64] = p.ljust(64)
        #                 new_[65:72] = '{:07d}'.format(reverse_pointers[i-1]).rjust(7)
        #                 sequence += 1
        #                 new_[72] = "P"
        #                 new_[73:line_length-1] = str(sequence).rjust(7)
        #                 new_[-1] = "\n"
        #                 new_lines += "".join(new_)
        #                 self.parameter_counter += 1
        #                 no_lines += 1

        #             param_string += new_lines 


        #         else: ############################################### no spline
        #             if len(e.parameter_string) > 64:
        #                 wrapped_params = my_wrapper(e.parameter_string)
        #             else:
        #                 wrapped_params = [e.parameter_string]
        #             new_lines = ""
        #             for p in wrapped_params:
        #                 new_ = [" "] * line_length
        #                 new_[0:64] = p.ljust(64)
        #                 new_[65:72] = '{:07d}'.format(reverse_pointers[i-1]).rjust(7)
        #                 sequence += 1
        #                 new_[72] = "P"
        #                 new_[73:line_length-1] = str(sequence).rjust(7)
        #                 new_[-1] = "\n"
        #                 new_lines += "".join(new_)
        #                 self.parameter_counter += 1
        #                 no_lines += 1

        #             param_string += new_lines 
                
        #         self.parameter_ref[i] = no_lines

        #         # print(f'################ {i} #################')
        #         # print(param_string)
        #     offset = [1]
        #     for v in self.parameter_ref.values():
        #         offset.append(v+offset[-1])
        #     self.parameter_ref = offset
                
        #     return param_string
        
        # NEW parameter_lines
        def parameter_lines():
            param_string = ""
            sequence = 0
            current_start_line = 1 

            # Iterate over FILTERED entities
            for i, e in enumerate(filtered_entities, start=1):
                self.calculated_param_start.append(current_start_line)
                
                # remove newlines from source data
                full_p_string = ""
                if isinstance(e.parameter_string, tuple):
                    p1, p2, p3 = e.parameter_string
                    full_p_string = p1 + p2.replace('\n', '') + p3
                else:
                    full_p_string = e.parameter_string.replace('\n', '')

                if not full_p_string.strip().endswith(';'):
                     full_p_string += ';'

                # Generate formatted lines
                ptr_str = '{:07d}'.format(i*2-1).rjust(7)
                chunks = chunker(full_p_string)
                
                lines_this_entity = 0 
                for chunk in chunks:
                    line = [" "] * line_length
                    line[0:64] = chunk.ljust(64)
                    line[64:72] = ptr_str 
                    sequence += 1
                    line[72] = "P"
                    line[73:line_length-1] = str(sequence).rjust(7)
                    line[-1] = "\n"
                    param_string += "".join(line)
                    self.parameter_counter += 1
                    current_start_line += 1
                    lines_this_entity += 1
                
                # Store the EXACT line count for the directory section
                self.calculated_line_count.append(lines_this_entity)
                
            return param_string

        def global_lines():
            global_string = '\n'.join(self.global_string)
            global_string += '\n'
            self.global_counter += len(self.global_string)
            return global_string

        def final_line():
            new_ = [" "] * line_length
            new_[0] = 'S'
            new_[1:8] = '{:07d}'.format(1).rjust(7)
            new_[8] = 'G'
            new_[9:16] = '{:07d}'.format(self.global_counter).rjust(7)
            new_[16] = 'D'
            new_[17:24] = '{:07d}'.format(self.directory_counter).rjust(7)
            new_[24] = 'P'
            new_[25:32] = '{:07d}'.format(self.parameter_counter).rjust(7)
            new_[72] = 'T'
            new_[73:line_length-1] = str(1).rjust(7)
            new_[-1] = "\n"
            s = ''.join(new_)            
            return s
                
        # Execution Order
        string = ""
        string += start_line()
        string += global_lines()        
        tmp_params = parameter_lines()         
        string += directory_lines()
        string += tmp_params
        string += final_line()
        with open(filename, "w") as f:
            f.write(string)


    def __getitem__(self, index):
        """Get an item by its pointer"""
        return self._entities[self._pointers[index]]

    @property
    def items(self):
        """IGES items

        Examples
        --------
        >>> from pyiges import examples
        >>> import pyiges
        >>> sample = pyiges.read(examples.sample)
        >>> item = sample.items[0]
        >>> item
        --- IGES Point ---
        0.0, 0.0, 0.0
        """
        return self._entities


def read(filename):
    """Read an iges file.


    Parameters
    ----------
    filename : str
        Filename of an IGES file.

    Examples
    --------
    >>> import pyiges
    >>> from pyiges import examples
    >>> iges = pyiges.read(examples.impeller)
        pyiges.Iges object
        Description:
        Number of Entities: 4615
    """
    return Iges(filename)