import { Listbox } from '@headlessui/react';
import { FunnelIcon,TrashIcon, ChevronUpDownIcon, CheckIcon, MagnifyingGlassIcon } from '@heroicons/react/20/solid';

interface FiltersBarProps {
  selectedCap: string;
  setSelectedCap: (val: string) => void;
  uniqueCaps: string[];
  itemsPerPage: number;
  setItemsPerPage: (val: number) => void;
  searchQuery: string;
  setSearchQuery: (val: string) => void;
}

export const FiltersBar = ({
  selectedCap,
  setSelectedCap,
  uniqueCaps,
  itemsPerPage,
  setItemsPerPage,
  searchQuery,
  setSearchQuery,
}: FiltersBarProps) => {
  const rowsPerPageOptions = [10, 25, 50, 100];

  const handleClearAll = () => {
    setSelectedCap('All');
    setItemsPerPage(10);
    setSearchQuery('');
  };

  return (
    <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 rounded-t-md flex items-center justify-between gap-6 px-4 py-3">

  <div className="flex items-center gap-2 md:flex-row flex-col">
    <FunnelIcon className="w-5 h-5 text-black dark:text-white" />
    <span className="font-medium text-gray-700 dark:text-gray-200">Filters</span>
    <button
      onClick={handleClearAll}
      className="text-xs text-red-600 hover:underline md:ml-2"
    >
      clear all<TrashIcon className="w-4 h-4 text-red-600 inline-block" />
    </button>
  </div>

  {/* Right: Dropdowns */}
  <div className="flex items-center gap-6 flex-wrap justify-end">
    {/* Search Input */}
        <div className="flex flex-col text-sm text-gray-700 dark:text-gray-200">
          <label className="mb-1 font-medium">Search</label>
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search stock..."
              className="md:w-48 pl-9 pr-3 py-1.5 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-black dark:text-white text-sm focus:outline-none focus:ring focus:ring-blue-500 w-32"
            />
            <MagnifyingGlassIcon className="absolute left-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          </div>
        </div>
    {/* Market Cap Filter */}
    <div className="flex flex-col text-sm text-gray-700 dark:text-gray-200">
      <label className="mb-1 font-medium">Market Cap</label>
      <Listbox value={selectedCap} onChange={setSelectedCap}>
        <div className="relative w-32">
          <Listbox.Button className="relative w-full cursor-pointer rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 py-1.5 pl-3 pr-10 text-left text-sm text-black dark:text-white">
            {selectedCap}
            <ChevronUpDownIcon className="absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          </Listbox.Button>
          <Listbox.Options className="absolute z-10 mt-1 w-full rounded bg-white dark:bg-gray-800 shadow-lg text-sm max-h-60 overflow-auto ring-1 ring-black/5">
            {uniqueCaps.map((cap) => (
              <Listbox.Option
                key={cap}
                value={cap}
                className={({ active }) =>
                  `relative cursor-pointer select-none py-1.5 pl-10 pr-4 ${
                    active
                      ? 'bg-blue-100 text-blue-900 dark:bg-blue-600 dark:text-white'
                      : 'text-gray-900 dark:text-gray-100'
                  }`
                }
              >
                {({ selected }) => (
                  <>
                    <span className={`block truncate ${selected ? 'font-medium' : 'font-normal'}`}>
                      {cap}
                    </span>
                    {selected && (
                      <span className="absolute left-2 inset-y-0 flex items-center text-blue-600 dark:text-white">
                        <CheckIcon className="h-4 w-4" />
                      </span>
                    )}
                  </>
                )}
              </Listbox.Option>
            ))}
          </Listbox.Options>
        </div>
      </Listbox>
    </div>

    {/* Rows Per Page */}
    <div className="flex flex-col text-sm text-gray-700 dark:text-gray-200">
      <label className="mb-1 font-medium">Rows Per Page</label>
      <Listbox value={itemsPerPage} onChange={setItemsPerPage}>
        <div className="relative w-32">
          <Listbox.Button className="relative w-full cursor-pointer rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 py-1.5 pl-3 pr-10 text-left text-sm text-black dark:text-white">
            {itemsPerPage}
            <ChevronUpDownIcon className="absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          </Listbox.Button>
          <Listbox.Options className="absolute z-10 mt-1 w-full rounded bg-white dark:bg-gray-800 shadow-lg text-sm max-h-60 overflow-auto ring-1 ring-black/5">
            {rowsPerPageOptions.map((count) => (
              <Listbox.Option
                key={count}
                value={count}
                className={({ active }) =>
                  `relative cursor-pointer select-none py-1.5 pl-10 pr-4 ${
                    active
                      ? 'bg-blue-100 text-blue-900 dark:bg-blue-600 dark:text-white'
                      : 'text-gray-900 dark:text-gray-100'
                  }`
                }
              >
                {({ selected }) => (
                  <>
                    <span className={`block truncate ${selected ? 'font-medium' : 'font-normal'}`}>
                      {count}
                    </span>
                    {selected && (
                      <span className="absolute left-2 inset-y-0 flex items-center text-blue-600 dark:text-white">
                        <CheckIcon className="h-4 w-4" />
                      </span>
                    )}
                  </>
                )}
              </Listbox.Option>
            ))}
          </Listbox.Options>
        </div>
      </Listbox>
    </div>
  </div>
</div>

  );
};
