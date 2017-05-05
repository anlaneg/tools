Puppet::Type.type(:ini_file_conf).provide(:ini_write) do
  
  def create
    Puppet.info "hello ini_write create!"
  end
  
  def destroy
    Puppet.info "hello ini_write destroy! #{@resource}"
  end
  
  def exists?
    Puppet.info "hello ini_write exists?"
    return false
  end
end