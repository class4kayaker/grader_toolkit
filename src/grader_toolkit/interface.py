from grader_toolkit import Student, Assignment, Grade  # noqa: F401
import zipfile
import os.path
from io import StringIO


def gen_smartsite_upload(assignment, gtemplate, outfn):
    # type: (Assignment, str) -> None
    aname = assignment.name
    gmap = {}
    for g in assignment.grades:
        dispid = g.student.email.split('@')[0]
        gmap[dispid] = g
    idmap = {}
    gradestr = StringIO()
    gformat = "{0},{1},{2.student.name},{2.grade}\n"
    for line in gtemplate:
        l = line.split(',')
        if len(l) == 5 and l[0] in gmap:
            g = gmap[l[0]]
            idmap[l[0]] = l[1]
            gradestr.write(gformat.format(dispid,
                                          l[1],
                                          g))
        else:
            gradestr.write(line)
    with zipfile.ZipFile(outfn, 'w') as outarchive:
        path = os.path.join(aname, 'grades.csv')
        outarchive.writestr(path, gradestr.getvalue())
        gradestr.close()
        for g in assignment.grades:
            dispid = g.student.email.split('@')[0]
            outid = idmap[dispid]
            stfolderfmt = "{0}({1})"
            if g.notes:
                path = os.path.join(aname,
                                    stfolderfmt.format(g.student.name, outid),
                                    "comments.txt")
                outarchive.writestr(path, g.notes)


upload_formats = {
    'smartsite': gen_smartsite_upload
}
