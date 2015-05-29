import logging
from commands import local
from errors import SVNException

PROJECT_ROOT = "http://jira.uji.es/repos/uji"


class Subversion:
    def __init__(self, checkout_dir, project_id):
        self.checkout_dir = checkout_dir
        self.project_id = project_id
        self.project_name = Subversion.get_project_name(self.project_id)

    @staticmethod
    def get_project_name(project_id):
        svnroot = "%s/%s/uji-%s" % (PROJECT_ROOT, project_id.upper(), project_id.lower())
        result = local("svn list " + svnroot)

        if result.return_code == 0:
            return "uji-%s" % project_id.lower()
        else:
            svnroot = "%s/%s/uji-%s-base" % (PROJECT_ROOT, project_id.upper(), project_id.lower())
            result = local("svn list " + svnroot)

            if result.return_code == 0:
                return "uji-%s-base" % project_id.lower()
            else:
                raise SVNException()

    def get_svnrepo_url(self, version):
        url_base = PROJECT_ROOT + "/" + self.project_id.upper() + "/" + self.project_name
        project_version = "trunk"

        if version != "trunk":
            project_version = "tags/%s_%s" % (self.project_name, version)

        return "%s/%s" % (url_base, project_version)

    def checkout(self, version):
        logging.info("[SCM] Checking out %s version" % version)

        result = local("svn co " + self.get_svnrepo_url(version) + " " + self.checkout_dir)

        if result.return_code != 0:
            logging.info("Single project repository not found, trying multi-module repository...")
            result = local("svn co " + self.get_svnrepo_url(version) + " " + self.checkout_dir)

            if result.return_code != 0:
                raise SVNException()

if __name__ == "__main__":
    subversion = Subversion("/tmp/LOD/uji-lod", "LOD")
    subversion.checkout("trunk")
