import os

class Function:

    created_functions = {}
    version_functions = {}

    # select count(revision), revision, a.file_id, f.start_line, f.end_line 
    # from annotates_2006_08_04 as a, functions as f 
    # where a.line_id>f.start_line and a.line_id<f.end_line and a.file_id=f.file_id and f.function_id=1 
    # group by revision;

    def getCommandOutput(self, cmd):

        pipe = os.popen(cmd)
        output = pipe.readlines()
        pipe.close()

        return output

    def getFunctions(self, filename):

        filepath = filename
        cmd = "ctags-exuberant --c-kinds=f -x "+filepath
        output_list = self.getCommandOutput(cmd)

        header_lines = []
        headers = []
        names = []

        for line in output_list:

            tokens = line.split(' ')
            # Remove empty tokens
            non_empty = []
            for t in tokens:
                if t != '':
                    non_empty.append(t)

            name = non_empty[0]
            line = non_empty[2]
            header = non_empty[4]

            names.append(name)
            header_lines.append(line)
            headers.append(header)

        return header_lines, headers, names

    def searchForBeginAndEnd(self, header_line, filename):

        filepath = filename
        fileobj = open(filepath,'r')
        content = fileobj.readlines()
        fileobj.close()

        try:
            header_line =int(header_line)
        except ValueError:
            header_line = 0

        rest_of_file = content[header_line - 1:]
        open_keys = 0
        closed_keys = 0

        current_line = header_line
        starting_line = header_line
        closing_line = header_line
        code = ""

        for line in rest_of_file:

            # Let's count the open and closed keys per line
            if line.find("{") != -1:
                open_keys += 1

                if 1 == open_keys:
                    starting_line = current_line

            if line.find("}") != -1:
                closed_keys += 1

            # Once we have found the opening key, if the numer of
            # open and closed is the same, the function end has been found
            if open_keys >= 1:

                code += line

                if open_keys == closed_keys:
                    closing_line = current_line
                    break

            current_line += 1

        return starting_line, closing_line, code

    def functions2sql(db):
        count = 0
        fkeys = Function.created_functions.keys()

        for f in fkeys:
            fn_name = Function.created_functions[f][0]
            file_id = Function.created_functions[f][1]
            fstart = Function.created_functions[f][2]
            fend = Function.created_functions[f][3]
            query = "INSERT INTO functions (function_id, name, file_id, start_line, end_line) "
            query += " VALUES ('" + str(count) + "','"
            query += str(fn_name) + "','"
            query += str(file_id) + "','"
            query += str(fstart) + "','"
            query += str(fend) + "');"
            count += 1

            db.insertData(query)

    def __init__(self, filename, file_id):

        header_lines, headers, names = self.getFunctions(filename)
        for i in range(len(header_lines)):
            header_line = header_lines[i]
            header = headers[i]
            name = names[i]

            begin_line, end_line, code = self.searchForBeginAndEnd(header_line, filename)
            #print filename + "    -> Function "+ name + " " + str(begin_line) + " "  + str(end_line)
            Function.created_functions[name] = [name, file_id, begin_line, end_line]

    functions2sql = staticmethod(functions2sql)
