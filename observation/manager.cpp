// Copyright (C) 2011, INRIA
// Author(s): Vivien Mallet
//
// This file is part of AtmoPy library, a tool for data processing and
// visualization in atmospheric sciences.
//
// AtmoPy is developed in the INRIA - ENPC joint project-team CLIME and in the
// ENPC - EDF R&D joint laboratory CEREA.
//
// AtmoPy is free software; you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the Free Software
// Foundation; either version 2 of the License, or (at your option) any later
// version.
//
// AtmoPy is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
// details.
//
// For more information, visit the AtmoPy home page:
//     http://cerea.enpc.fr/polyphemus/atmopy.html


#ifndef ATMOPY_FILE_MANAGER_CPP

#define OPS_WITH_EXCEPTION
#define SELDON_DEBUG_LEVEL_2

#include "../../driver/common/observation/GroundNetworkObservationManager.cxx"

namespace Seldon
{
  template class MallocAlloc<int>;
  template class Vector_Base<int, MallocAlloc<int> >;
  template class Vector<int, VectFull, MallocAlloc<int> >;
  template class MallocAlloc<double>;
  template class Vector_Base<double, MallocAlloc<double> >;
  template class Vector<double, VectFull, MallocAlloc<double> >;

  template class MallocObject<Vector<double> >;
  template class Vector2<double>;
}

namespace Polyphemus
{
  template class GroundNetworkObservationManager<double>;
  template void GroundNetworkObservationManager<double>::ApplyOperator(const Seldon::Vector<double>& x, Seldon::Vector<double>& y) const;
}


#define ATMOPY_FILE_MANAGER_CPP
#endif