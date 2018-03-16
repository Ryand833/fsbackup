import os
from binascii import hexlify
from struct import unpack

def conv_le_uint8(bytes):
	return unpack('<B', bytes)[0]

def conv_le_uint16(bytes):
	return unpack('<H', bytes)[0]

def conv_le_uint32(bytes):
	return unpack('<L', bytes)[0]

def conv_le_uint64(bytes):
	return unpack('<Q', bytes)[0]

def conv_le_sint8(bytes):
	return unpack('<b', bytes)[0]

def conv_le_sint16(bytes):
	return unpack('<h', bytes)[0]

def conv_le_sint32(bytes):
	return unpack('<l', bytes)[0]

def conv_le_sint64(bytes):
	return unpack('<q', bytes)[0]

def conv_be_uint8(bytes):
	return unpack('>B', bytes)[0]

def conv_be_uint16(bytes):
	return unpack('>H', bytes)[0]

def conv_be_uint32(bytes):
	return unpack('>L', bytes)[0]

def conv_be_uint64(bytes):
	return unpack('>Q', bytes)[0]

def conv_be_sint8(bytes):
	return unpack('>b', bytes)[0]

def conv_be_sint16(bytes):
	return unpack('>h', bytes)[0]

def conv_be_sint32(bytes):
	return unpack('>l', bytes)[0]

def conv_be_sint64(bytes):
	return unpack('>q', bytes)[0]

def conv_string(string):
	return string.split(b'\0',1)[0]

def conv_uuid(uuid_bytes):
	split = lambda x: [x[:8], x[8:12], x[12:16], x[16:20], x[20:]]
	return '-'.join(split(hexlify(uuid_bytes)))

def ext2_mntopt_string(mntopt):
	if mntopt == 0x0001:
		return 'debug'
	elif mntopt == 0x0002:
		return 'bsdgroups'
	elif mntopt == 0x0004:
		return 'user_xattr'
	elif mntopt == 0x0008:
		return 'acl'
	elif mntopt == 0x0010:
		return 'uid16'
	elif mntopt == 0x0020:
		return 'journal_data'
	elif mntopt == 0x0040:
		return 'journal_data_ordered'
	elif mntopt == 0x0060:
		return 'journal_data_writeback'
	elif mntopt == 0x0100:
		return 'nobarrier'
	elif mntopt == 0x0200:
		return 'block_validity'
	elif mntopt == 0x0400:
		return 'discard'
	elif mntopt == 0x0800:
		return 'nodelalloc'

def ext2_get_info(devname):
	ext2_info = {}
	SB_START = 1024
	with open(devname, 'rb') as f:
		# Block size
		f.seek(SB_START + 24)
		ext2_info['block_size'] = 1024 << conv_le_uint32(f.read(4))

		# Max mount count
		f.seek(SB_START + 54)
		ext2_info['max_mnt_count'] = conv_le_sint16(f.read(2))

		# Check interval
		f.seek(SB_START + 68)
		ext2_info['checkinterval'] = conv_le_uint32(f.read(4))

		# Revision level
		f.seek(SB_START + 76)
		ext2_info['rev_level'] = conv_le_uint32(f.read(4))

		# I-node size
		if ext2_info['rev_level'] >= 1:
			f.seek(SB_START + 88)
			ext2_info['inode_size'] = conv_le_uint16(f.read(2))
		else:
			ext2_info['inode_size'] = 128

		# UUID
		f.seek(SB_START + 104)
		ext2_info['uuid'] = conv_uuid(f.read(16))

		# Volume label
		f.seek(SB_START + 120)
		ext2_info['label'] = conv_string(f.read(16))

		# Default mount options
		f.seek(SB_START + 256)
		dfltmntopts = conv_le_uint32(f.read(4))
		mntopts = []
		if dfltmntopts & 0x0060:    # JMODE
			mntopts.append(ext2_mntopt_string(0x0060))
		m = 1
		for i in xrange(0, 32):
			if dfltmntopts & m:
				mntopts.append(ext2_mntopt_string(m))
			m = m << 1
		ext2_info['default_mount_opts'] = ','.join(mntopts)

		# RAID stride
		f.seek(SB_START + 356)
		ext2_info['raid_stride'] = conv_le_uint16(f.read(2))

		# RAID stripe width
		f.seek(SB_START + 368)
		ext2_info['raid_stripe_width'] = conv_le_uint32(f.read(4))

	return ext2_info

def ext2_get_mkfs(cmdname, devname, ext2_info):
	# Quiet mode
	options = ' -t {0} -q '.format(ext2_info['type'])

	# Revision level
	options += ' -r {0} '.format(ext2_info['rev_level'])

	# Volume label
	options += ' -L "{0}" '.format(ext2_info['label'])

	# Block size
	options += ' -b {0} '.format(ext2_info['block_size'])

	# I-node size
	options += ' -I {0} '.format(ext2_info['inode_size'])

	# RAID stride
	options += ' -E stride={0} '.format(ext2_info['raid_stride'])

	# RAID stripe width
	options += ' -E stripe-width={0} '.format(ext2_info['raid_stripe_width'])
	
	# Assemble command
	cmd = '{0} {1} {2}'.format(cmdname, options, devname)
	return cmd

def ext2_get_extra(cmdname, devname, ext2_info):
	options = ''

	# UUID
	options += ' -U {0} '.format(ext2_info['uuid'])

	# Default mount options
	if not ext2_info['default_mount_opts'].strip() == '':
		options += ' -o {0} '.format(ext2_info['default_mount_opts'])

	# Max mount count
	options += ' -c {0} '.format(ext2_info['max_mnt_count'])

	# Check interval
	options += ' -i {0} '.format(ext2_info['checkinterval'] / 86400)
	
	# Assemble command
	cmd = '{0} {1} {2}'.format(cmdname, options, devname)
	return cmd

def xfs_get_info(devname):
	xfs_info = {}
	SB_START = 0
	with open(devname, 'rb') as f:
		# Block size
		f.seek(SB_START + 4)
		xfs_info['block_size'] = conv_be_uint32(f.read(4))

		# UUID
		f.seek(SB_START + 32)
		xfs_info['uuid'] = conv_uuid(f.read(16))

		# Volume label
		f.seek(SB_START + 108)
		xfs_info['label'] = conv_string(f.read(12))

	return xfs_info

def xfs_get_mkfs(cmdname, devname, xfs_info):
	options = ' -t xfs '

	# UUID
	# Setting the UUID requires xfs-progs to be at least version 4.3.0+
	options += ' -m uuid={0} '.format(xfs_info['uuid'])

	# Force
	options += ' -f '

	# Volume label
	options += ' -L "{0}" '.format(xfs_info['label'])

	# Block size
	options += ' -b size={0} '.format(xfs_info['block_size'])

	# Assemble command
	cmd = '{0} {1} {2}'.format(cmdname, options, devname)
	return cmd

def xfs_get_extra(cmdname, devname, xfs_info):
	options = ''

	# Assemble command
	#cmd = '{0} {1} {2}'.format(cmdname, options, devname)
	cmd = ''
	return cmd

