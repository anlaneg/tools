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
  
  def path
    Puppet.info "get path property"
  end
  
  def path=
    Puppet.info "set path property"
  end
  
  def color
    Puppet.info "get color property"
  end
  
  def color=
    Puppet.info "set color property"
  end
end